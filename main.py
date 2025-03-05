import sqlite3

# ====================================================
# Database Setup Functions
# ====================================================

def create_database():
    conn = sqlite3.connect('animals.db')
    c = conn.cursor()

    # Create the animals table.
    c.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create the characteristics table with an optional question prompt.
    c.execute('''
        CREATE TABLE IF NOT EXISTS characteristics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            question TEXT
        )
    ''')

    # Create the animal_characteristics table.
    # Instead of a binary flag, we store a weight (REAL) between 0 and 1.
    c.execute('''
        CREATE TABLE IF NOT EXISTS animal_characteristics (
            animal_id INTEGER,
            characteristic_id INTEGER,
            weight REAL,
            FOREIGN KEY (animal_id) REFERENCES animals(id),
            FOREIGN KEY (characteristic_id) REFERENCES characteristics(id)
        )
    ''')

    conn.commit()
    conn.close()


def insert_entries_from_files():
    """
    Reads from three text files to populate the database.
    
    Expected file formats:
    
    animals.txt:
      One animal name per line.
    
    characteristics.txt:
      Each line: characteristic|question
    
    animal_characteristics.txt:
      Each line: Animal: characteristic1[:weight], characteristic2[:weight], ...
      If no weight is provided, a default of 1.0 is used.
    """
    conn = sqlite3.connect('animals.db')
    c = conn.cursor()

    # ----------------------------
    # Insert animals from animals.txt
    # ----------------------------
    animal_ids = {}
    try:
        with open("animals.txt", "r", encoding="utf-8") as f:
            for line in f:
                animal = line.strip()
                if animal:
                    c.execute("INSERT INTO animals (name) VALUES (?)", (animal,))
                    animal_ids[animal] = c.lastrowid
    except FileNotFoundError:
        print("animals.txt not found. Please create this file with one animal per line.")
        conn.close()
        return

    # ----------------------------
    # Insert characteristics from characteristics.txt
    # ----------------------------
    char_ids = {}
    try:
        with open("characteristics.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) >= 2:
                        char_name = parts[0].strip()
                        char_question = parts[1].strip()
                        c.execute("INSERT INTO characteristics (name, question) VALUES (?, ?)", 
                                  (char_name, char_question))
                        char_ids[char_name] = c.lastrowid
                    else:
                        print("Skipping malformed line in characteristics.txt:", line)
    except FileNotFoundError:
        print("characteristics.txt not found. Please create this file in the expected format.")
        conn.close()
        return

    # ----------------------------
    # Insert animal-characteristics from animal_characteristics.txt
    # ----------------------------
    try:
        with open("animal_characteristics.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    # Expecting format: "Animal: characteristic1[:weight], characteristic2[:weight], ..."
                    if ":" not in line:
                        print("Skipping malformed line in animal_characteristics.txt:", line)
                        continue
                    animal_name, char_list = line.split(":", 1)
                    animal_name = animal_name.strip()
                    # Skip if animal not found.
                    if animal_name not in animal_ids:
                        print(f"Warning: Animal '{animal_name}' not found in animals.txt")
                        continue
                    # Split characteristics by comma.
                    char_entries = [x.strip() for x in char_list.split(",") if x.strip()]
                    for entry in char_entries:
                        # If weight is provided, it should be after a colon.
                        if ":" in entry:
                            parts = entry.split(":")
                            char_name = parts[0].strip()
                            try:
                                weight = float(parts[1].strip())
                            except ValueError:
                                weight = 1.0
                        else:
                            char_name = entry
                            weight = 1.0
                        if char_name not in char_ids:
                            print(f"Warning: Characteristic '{char_name}' not found in characteristics.txt")
                            continue
                        c.execute(
                            "INSERT INTO animal_characteristics (animal_id, characteristic_id, weight) VALUES (?, ?, ?)",
                            (animal_ids[animal_name], char_ids[char_name], weight)
                        )
    except FileNotFoundError:
        print("animal_characteristics.txt not found. Please create this file in the expected format.")
        conn.close()
        return

    conn.commit()
    conn.close()
    print("Database populated from text files.")


# ====================================================
# Game Logic Functions
# ====================================================

def fetch_data():
    """
    Fetches animals with their characteristic weights and the questions for each characteristic.
    
    Returns:
        animals_dict (dict): Mapping animal names to a dict of {characteristic: weight}.
                             e.g. {'Cat': {'has fur': 1.0, 'meows': 1.0, 'is small': 0.8}, ... }
        char_questions (dict): Mapping characteristic names to their question text.
    """
    conn = sqlite3.connect('animals.db')
    c = conn.cursor()
    
    # Fetch animals.
    c.execute("SELECT id, name FROM animals")
    animals_data = c.fetchall()
    animal_id_to_name = {row[0]: row[1] for row in animals_data}
    
    # Fetch characteristics.
    c.execute("SELECT id, name, question FROM characteristics")
    char_data = c.fetchall()
    char_id_to_name = {row[0]: row[1] for row in char_data}
    char_questions = {row[1]: row[2] for row in char_data}
    
    # Build mapping: animal name -> {characteristic: weight}
    c.execute("SELECT animal_id, characteristic_id, weight FROM animal_characteristics")
    links = c.fetchall()
    
    animals_dict = {name: {} for name in animal_id_to_name.values()}
    for animal_id, char_id, weight in links:
        animal_name = animal_id_to_name[animal_id]
        char_name = char_id_to_name[char_id]
        animals_dict[animal_name][char_name] = weight
    
    conn.close()
    return animals_dict, char_questions


def bayes_update(animals, answers):
    """
    Update animal probabilities based on user answers using a weighted (partial truth) approach.
    
    For each characteristic, we blend the likelihood of a "yes" answer if the animal has the trait
    with the likelihood if it does not, weighted by the stored weight.
    
    Parameters:
        animals (dict): Mapping animal names to {characteristic: weight}.
        answers (dict): Mapping characteristic names to the user's answer.
                        Answer options: "yes", "no", "probably", "probably not", "i dont know".
                        
    Returns:
        dict: Normalized probabilities for each animal.
    """
    # Likelihood multipliers for a full match (if weight were 1).
    likelihood_if_feature = {
        "yes": 0.9,
        "probably": 0.7,
        "probably not": 0.3,
        "no": 0.1,
        "i dont know": 1.0  # Neutral evidence.
    }
    
    # Likelihood multipliers for no match (if weight were 0).
    likelihood_if_not_feature = {
        "yes": 0.1,
        "probably": 0.3,
        "probably not": 0.7,
        "no": 0.9,
        "i dont know": 1.0  # Neutral evidence.
    }
    
    scores = {}
    n_animals = len(animals)
    prior = 1.0 / n_animals  # Uniform prior.
    
    for animal, traits in animals.items():
        score = prior
        for characteristic, response in answers.items():
            # Get the weight (degree of membership) for this trait; default to 0 if not present.
            w = traits.get(characteristic, 0)
            # Compute a blended likelihood factor.
            factor = w * likelihood_if_feature[response] + (1 - w) * likelihood_if_not_feature[response]
            score *= factor
        scores[animal] = score

    # Normalize the scores.
    total = sum(scores.values())
    if total == 0:
        return {animal: 1.0 / n_animals for animal in animals}
    for animal in scores:
        scores[animal] /= total

    return scores


def choose_next_question(probabilities, animals, asked):
    """
    Selects the next characteristic (question) to ask.
    
    It considers all characteristics (from the weighted mapping) not yet asked and computes
    a weighted probability that each characteristic is present among the remaining animals.
    The characteristic whose overall probability is closest to 0.5 (most uncertain) is selected.
    
    Parameters:
        probabilities (dict): Current probability distribution over animals.
        animals (dict): Mapping of animal names to {characteristic: weight}.
        asked (set): Set of characteristics that have already been asked.
        
    Returns:
        str or None: The selected characteristic name, or None if no new characteristic is available.
    """
    candidate_chars = set()
    for traits in animals.values():
        candidate_chars.update(traits.keys())
    candidate_chars -= asked
    if not candidate_chars:
        return None

    best_char = None
    best_uncertainty = float('inf')
    
    for char in candidate_chars:
        # Compute a weighted sum of the probability that this characteristic is present.
        p = sum(probabilities[animal] * animals[animal].get(char, 0)
                for animal in animals)
        # We want p to be near 0.5 for maximum information gain.
        uncertainty = abs(p - 0.5)
        if uncertainty < best_uncertainty:
            best_uncertainty = uncertainty
            best_char = char

    return best_char


def play_game():
    """
    Main game loop.
    
    The game fetches animals and characteristics from the database (with weighted values),
    then dynamically generates questions. User answers update animal probabilities via a Bayesian update.
    The loop continues until one animal's probability exceeds a threshold or no more questions are available.
    """
    animals, char_questions = fetch_data()
    
    answers = {}
    probabilities = {animal: 1.0 / len(animals) for animal in animals}  # Start uniform.
    asked = set()
    threshold = 0.8  # Confidence threshold to make a guess.
    
    while True:
        # Check if any animal's probability is high enough.
        best_animal = max(probabilities, key=probabilities.get)
        if probabilities[best_animal] >= threshold:
            print(f"\nI guess the animal is: {best_animal} (confidence: {probabilities[best_animal]:.3f})")
            break
        
        # Choose next question.
        next_char = choose_next_question(probabilities, animals, asked)
        if not next_char:
            print("\nNo more questions available. Final probabilities:")
            for animal, prob in probabilities.items():
                print(f"{animal}: {prob:.3f}")
            break
        
        asked.add(next_char)
        question = char_questions.get(next_char, f"Does it have the characteristic '{next_char}'?")
        print("\n" + question)
        print("Options: yes, no, probably, probably not, i dont know")
        response = input("Your answer: ").strip().lower()
        valid_options = {"yes", "no", "probably", "probably not", "i dont know"}
        while response not in valid_options:
            print("Invalid option. Please choose one of: yes, no, probably, probably not, i dont know")
            response = input("Your answer: ").strip().lower()
        answers[next_char] = response
        
        # Update probabilities based on the new answer.
        probabilities = bayes_update(animals, answers)
        print("\nUpdated probabilities:")
        for animal, prob in probabilities.items():
            print(f"{animal}: {prob:.3f}")
        print("-" * 30)


# ====================================================
# Main Execution
# ====================================================

if __name__ == '__main__':
    # Create the database structure.
    create_database()
    # Populate the database from text files.
    insert_entries_from_files()
    
    # Run the interactive game.
    play_game()
