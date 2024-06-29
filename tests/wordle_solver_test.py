from src.solver.wordle_solver import WordleSolver


class WordleSolverTest:
    def __init__(self, solver_class, valid_words_file, word_freq_file, letter_freq_file, target_words):
        self.solver_class = solver_class
        self.valid_words_file = valid_words_file
        self.word_freq_file = word_freq_file
        self.letter_freq_file = letter_freq_file
        self.target_words = target_words

    def simulate_game(self, target_word):
        solver = self.solver_class(self.valid_words_file, self.word_freq_file, self.letter_freq_file)
        guess_count = 0
        correct = False

        while not correct:
            guess = solver.get_optimal_guess()
            guess_count += 1
            feedback = self.get_feedback(guess, target_word)
            if guess == target_word:
                correct = True
            else:
                solver.adjust_guess(guess, feedback)

        return guess_count

    def get_feedback(self, guess, target_word):
        feedback = []
        for g_char, t_char in zip(guess, target_word):
            if g_char == t_char:
                feedback.append(WordleSolver.GREEN)
            elif g_char in target_word:
                feedback.append(WordleSolver.YELLOW)
            else:
                feedback.append(WordleSolver.BLACK)
        return feedback

    def calculate_average_guesses(self):
        results = [self.simulate_game(target) for target in self.target_words]
        average_guesses = sum(results) / len(self.target_words)
        return average_guesses

    def run_tests(self):
        average_guesses = self.calculate_average_guesses()
        print(f"Average number of guesses over {len(self.target_words)} games: {average_guesses:.2f}")


if __name__ == "__main__":
    target_words = ['proud']

    tester = WordleSolverTest(
        WordleSolver,
        '../frequencyMaps/validwords.txt',
        '../frequencyMaps/regularized_word_freq_map.json',
        '../frequencyMaps/regularized_letter_freq_map.json',
        target_words
    )
    tester.run_tests()
