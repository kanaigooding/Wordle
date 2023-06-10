import os
import numpy
from datetime import datetime
from wordle_solver import WordleSolver
from concurrent.futures import ProcessPoolExecutor
import itertools


class WordleSolverTester:

    def __init__(self, wordle_solver):
        self.solver = wordle_solver
        self.result_folder = 'testingResults'
        self.result_file = 'results.txt'
        self.stats_file = 'stats.txt'
        self.word_attempts = []

    def test_solver(self):
        os.makedirs(self.result_folder, exist_ok=True)

        # Create a ProcessPoolExecutor
        with ProcessPoolExecutor() as executor:
            # Use the map function to assign each word to a process in the pool
            results = executor.map(self.test_word, self.solver.words)

            # Iterate through the results as they become available
            for result in results:
                self.word_attempts.append(result[1])

                with open(os.path.join(self.result_folder, self.result_file), 'a') as f:
                    f.write(f'Word: {result[0]}, Attempts: {result[1]}, Guesses: {result[2]}\n')

        self.generate_stats()

    def test_word(self, word):
        self.solver.reset()
        attempts = 0
        guesses = []

        guess = "irate"  # first guess is always "irate"
        while True:
            guesses.append(guess)
            attempts += 1
            feedback = self.generate_feedback(word, guess)
            if feedback == 'GGGGG':
                break
            else:
                self.solver.adjust_guess(guess, feedback)
                guess = self.solver.get_optimal_guess()  # next guesses will be optimal based on previous feedback
        return word, attempts, guesses

    def generate_feedback(self, target, guess):
        feedback = []
        for t, g in zip(target, guess):
            if t == g:
                feedback.append('G')
            elif g in target:
                feedback.append('Y')
            else:
                feedback.append('B')
        return ''.join(feedback)

    def generate_stats(self):
        min_attempts = min(self.word_attempts)
        max_attempts = max(self.word_attempts)
        avg_attempts = numpy.mean(self.word_attempts)
        median_attempts = numpy.median(self.word_attempts)
        std_dev_attempts = numpy.std(self.word_attempts)

        with open(os.path.join(self.result_folder, self.stats_file), 'a') as f:
            f.write(f'Iteration: \n')
            f.write(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Average attempts: {avg_attempts}\n')
            f.write(f'Minimum attempts: {min_attempts}\n')
            f.write(f'Maximum attempts: {max_attempts}\n')
            f.write(f'Median attempts: {median_attempts}\n')
            f.write(f'Standard Deviation of attempts: {std_dev_attempts}\n')
            f.write(f'============================================================================\n')


if __name__ == "__main__":
    solver = WordleSolver('../frequencyMaps/validwords.txt', '../frequencyMaps/word_freq_map.json',
                          '../frequencyMaps/letter_freq_map.json')
    tester = WordleSolverTester(solver)
    tester.test_solver()
