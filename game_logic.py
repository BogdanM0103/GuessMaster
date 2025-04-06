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
    conn = sqlite3.connect('animals.db')
    c = conn.cursor()

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

    try:
        with open("animal_characteristics.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    if ":" not in line:
                        print("Skipping malformed line in animal_characteristics.txt:", line)
                        continue
                    animal_name, char_list = line.split(":", 1)
                    animal_name = animal_name.strip()
                    if animal_name not in animal_ids:
                        print(f"Warning: Animal '{animal_name}' not found in animals.txt")
                        continue
                    char_entries = [x.strip() for x in char_list.split(",") if x.strip()]
                    for entry in char_entries:
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
    conn = sqlite3.connect('animals.db')
    c = conn.cursor()

    c.execute("SELECT id, name FROM animals")
    animals_data = c.fetchall()
    animal_id_to_name = {row[0]: row[1] for row in animals_data}

    c.execute("SELECT id, name, question FROM characteristics")
    char_data = c.fetchall()
    char_id_to_name = {row[0]: row[1] for row in char_data}
    char_questions = {row[1]: row[2] for row in char_data}

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
    answers = {k: v.lower() for k, v in answers.items()}
    scores = {}
    n_animals = len(animals)
    prior = 1.0 / n_animals

    ANSWER_WEIGHTS = {
        "yes": {"feature": 0.95, "not_feature": 0.05},
        "probably": {"feature": 0.75, "not_feature": 0.25},
        "probably not": {"feature": 0.25, "not_feature": 0.75},
        "no": {"feature": 0.05, "not_feature": 0.95},
        "i dont know": {"feature": 1.0, "not_feature": 1.0},
    }

    for animal, traits in animals.items():
        score = prior
        for characteristic, response in answers.items():
            response_data = ANSWER_WEIGHTS.get(response, {"feature": 1.0, "not_feature": 1.0})
            w = traits.get(characteristic, 0)
            factor = w * response_data["feature"] + (1 - w) * response_data["not_feature"]
            score *= factor
        scores[animal] = score

    total = sum(scores.values())
    if total == 0:
        return {animal: 1.0 / n_animals for animal in animals}
    for animal in scores:
        scores[animal] /= total

    return scores


def choose_next_question(probabilities, animals, asked):
    """
    Selects the next characteristic (question) to ask.
    
    It considers all characteristics not yet asked and computes
    a weighted probability that each characteristic is present among the remaining animals.
    The characteristic whose overall probability is closest to 0.5 is selected.
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
        p = sum(probabilities[animal] * animals[animal].get(char, 0)
                for animal in animals)
        uncertainty = abs(p - 0.5)
        if uncertainty < best_uncertainty:
            best_uncertainty = uncertainty
            best_char = char

    return best_char
