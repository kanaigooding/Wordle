# wordle_solver.py

import json

class WordleSolver:
    def __init__(self, valid_words_file, word_freq_file, letter_freq_file):
        self.words = self.load_words(valid_words_file)
        self.word_freq = self.load_freq(word_freq_file)
        self.letter_freq = self.load_freq(letter_freq_file)
        self.possible_words = self.words.copy()

    def load_words(self, file):
        with open(file, 'r') as f:
            words = f.read().splitlines()
        return words

    def load_freq(self, file):
        with open(file, 'r') as f:
            freq = json.load(f)
        return freq

    def adjust_guess(self, guessed_word, feedback):
        new_possible_words = []
        for word in self.possible_words:
            if self.is_possible(word, guessed_word, feedback):
                new_possible_words.append(word)
        self.possible_words = new_possible_words

    def is_possible(self, word, guessed_word, feedback):
        for i in range(5):
            if feedback[i] == 'G' and word[i] != guessed_word[i]:
                return False
            if feedback[i] == 'B' and word[i] == guessed_word[i]:
                return False
            if feedback[i] == 'Y' and guessed_word[i] == word[i]:
                return False
            if feedback[i] == 'Y' and not word.__contains__(guessed_word[i]):
                return False
        return True

    def get_optimal_guess(self):
        if self.possible_words:
            print(self.possible_words)
            optimal_word = max(self.possible_words, key=self.get_word_score)
            return optimal_word
        else:
            return "No optimal guess could be made."

    def get_word_score(self, word):
        word_score = self.word_freq.get(word, 0)
        letter_score = sum(self.letter_freq.get(letter, 0) for letter in word)
        return word_score + letter_score

    def reset(self):
        self.possible_words = self.words.copy()
