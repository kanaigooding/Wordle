import os
import numpy
from wordle_solver import WordleSolver
from concurrent.futures import ProcessPoolExecutor


class WordleSolverTester:
    def __init__(self, wordle_solver):
        self.solver = wordle_solver
        self.result_folder = 'testingResults'
        self.result_file = 'results.txt'
        self.stats_file = 'stats.txt'
        self.word_attempts = []
        self.result_data = []

    def test_solver(self):
        os.makedirs(self.result_folder, exist_ok=True)

        # Create a ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=10) as executor:
            # Use the map function to assign each word to a process in the pool
            results = executor.map(self.test_word, self.solver.words)

            # Iterate through the results as they become available
            for result in results:
                self.word_attempts.append(result[1])
                self.result_data.append(f'Word: {result[0]}, Attempts: {result[1]}, Guesses: {result[2]}\n')

        # Write all results to the file in a single operation
        with open(os.path.join(self.result_folder, self.result_file), 'w') as f:
            f.writelines(self.result_data)

        self.generate_stats()

    def test_word(self, word):
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

    def generate_feedback(self, target, guess):
        feedback = ''
        for t, g in zip(target, guess):
            if t == g:
                feedback += 'G'
            elif g in target:
                feedback += 'Y'
            else:
                feedback += 'B'
        return feedback

    def generate_stats(self):
        min_attempts = min(self.word_attempts)
        max_attempts = max(self.word_attempts)
        avg_attempts = numpy.mean(self.word_attempts)
        median_attempts = numpy.median(self.word_attempts)
        std_dev_attempts = numpy.std(self.word_attempts)
        percent_success = len([r for r in self.word_attempts if r <= 6]) / 129.53

        with open(os.path.join(self.result_folder, self.stats_file), 'a') as f:
            f.write(f'Iteration: \n')
            f.write(f'Average attempts: {avg_attempts}\n')
            f.write(f'Minimum attempts: {min_attempts}\n')
            f.write(f'Maximum attempts: {max_attempts}\n')
            f.write(f'Median attempts: {median_attempts}\n')
            f.write(f'Standard Deviation of attempts: {std_dev_attempts}\n')
            f.write(f'Percentage of words solved with less or equal to 6 attempts: {percent_success}\n')
            f.write(f'============================================================================\n')


if __name__ == "__main__":
    solver = WordleSolver('../frequencyMaps/validwords.txt', '../frequencyMaps/word_freq_map.json',
                          '../frequencyMaps/letter_freq_map.json')
    tester = WordleSolverTester(solver)
    tester.test_solver()
