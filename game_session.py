from game_logic import fetch_data, bayes_update, choose_next_question

class GameSession:
    def __init__(self, threshold=0.8):
        # Încărcăm datele inițiale (animale și întrebări)
        self.animals, self.char_questions = fetch_data()

        # Inițializăm probabilități uniforme pentru fiecare animal
        self.probabilities = {
            animal_name: 1.0 / len(self.animals) for animal_name in self.animals
        }

        # Dicționar pentru a reține răspunsurile date (întrebare -> răspuns)
        self.answers = {}
        # Pragul de încredere pentru a termina jocul cu o ghicire
        self.threshold = threshold
        # Indicatori de stare a jocului
        self.finished = False
        self.predicted_animal = None
        # Reține ultima întrebare pusă (util pentru a corela cu răspunsul așteptat)
        self.current_question = None

    def get_current_question(self):
        if self.finished:
            return None

        # Verifică dacă există un animal cu probabilitate peste prag
        best_animal = max(self.probabilities, key=self.probabilities.get)
        best_prob = self.probabilities[best_animal]

        if best_prob >= self.threshold:
            self.finished = True
            self.predicted_animal = best_animal
            return None

        # Selectează următoarea întrebare optimă
        next_char = choose_next_question(self.probabilities, self.animals, self.asked_questions())
        self.current_question = next_char

        if next_char is None:
            self.finished = True
            self.predicted_animal = self.get_prediction()
            return None

        return self.char_questions.get(next_char, f"Does it have '{next_char}'?")

    def submit_answer(self, answer):
        if self.current_question is not None:
            self.answers[self.current_question] = answer
            self.probabilities = bayes_update(self.animals, self.answers)

    def get_prediction(self):
        if self.predicted_animal is not None:
            return self.predicted_animal
        return max(self.probabilities, key=self.probabilities.get)

    def asked_questions(self):
        return set(self.answers.keys())
