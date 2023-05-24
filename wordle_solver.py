# wordle_solver.py

import json


class WordleSolver:
    # Initialize the Wordle Solver with dictionaries of valid words, word frequency, and letter frequency
    def __init__(self, valid_words_file, word_freq_file, letter_freq_file):
        self.words = self.load_words(valid_words_file)
        self.word_freq = self.load_freq(word_freq_file)
        self.letter_freq = self.load_freq(letter_freq_file)
        self.possible_words = self.words.copy()

    # Load valid words from the given file
    def load_words(self, file):
        with open(file, 'r') as f:
            words = f.read().splitlines()
        return words

    # Load word or letter frequency from the given file
    def load_freq(self, file):
        with open(file, 'r') as f:
            freq = json.load(f)
        return freq

    # Adjust possible words based on the guessed word and feedback
    def adjust_guess(self, guessed_word, feedback):
        new_possible_words = []
        for word in self.possible_words:
            if self.is_possible(word, guessed_word, feedback):
                new_possible_words.append(word)
        print(new_possible_words)
        self.possible_words = new_possible_words

    # Check if a word is a possible solution based on the guessed word and feedback
    def is_possible(self, word, guessed_word, feedback):
        for i in range(5):
            if feedback[i] == 'B' and word.__contains__(guessed_word[i]):
                return False
            if feedback[i] == 'Y' and guessed_word[i] == word[i]:
                return False
            if feedback[i] == 'Y' and not word.__contains__(guessed_word[i]):
                return False
            if feedback[i] == 'G' and word[i] != guessed_word[i]:
                return False
        return True

    # Get the optimal guess based on the remaining possible words
    def get_optimal_guess(self):
        if self.possible_words:
            optimal_word = max(self.possible_words, key=self.get_word_score)
            return optimal_word
        else:
            return "No optimal guess could be made."

    # Get the score of a word based on word frequency and letter frequency
    def get_word_score(self, word):
        word_score = self.word_freq.get(word, 0)
        letter_score = sum(self.letter_freq.get(letter, 0) for letter in word)
        return word_score + letter_score

    # Reset the solver to the initial state
    def reset(self):
        self.possible_words = self.words.copy()
