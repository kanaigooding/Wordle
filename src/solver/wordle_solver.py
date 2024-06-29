import json
import math
from collections import defaultdict


class WordleSolver:
    BLACK = 'B'
    YELLOW = 'Y'
    GREEN = 'G'

    def __init__(self, valid_words_file, word_freq_file, letter_freq_file):
        self.words = self.load_words(valid_words_file)
        self.word_freq = self.load_freq(word_freq_file)
        self.letter_freq = self.load_freq(letter_freq_file)
        self.possible_words = self.words.copy()
        self.precomputed_scores = self.precompute_scores()

    def load_words(self, file):
        """Loads valid words from a file."""
        try:
            with open(file, 'r') as f:
                return f.read().splitlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File {file} not found!")

    def load_freq(self, file):
        """Loads frequency data from a file."""
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading frequency from {file}: {e}")

    def precompute_scores(self):
        """Precomputes the scores for all words based on letter and word frequency."""
        return {
            word: sum(self.letter_freq.get(letter, 0) for letter in set(word)) * 0.5 + self.word_freq.get(word, 0) * 0.5
            for word in self.words}

    def adjust_guess(self, guessed_word, feedback):
        """Adjusts the list of possible words based on the guessed word and feedback."""
        self.possible_words = [
            word for word in self.possible_words if self.is_possible(word, guessed_word, feedback)
        ]

    def is_possible(self, word, guessed_word, feedback):
        """Checks if a word is a possible solution based on the guessed word and feedback."""
        black_letters = set()
        yellow_letters = defaultdict(set)

        for i, (g_char, f_char) in enumerate(zip(guessed_word, feedback)):
            if f_char == self.GREEN:
                if g_char != word[i]:
                    return False
            elif f_char == self.YELLOW:
                if g_char == word[i] or g_char not in word:
                    return False
                yellow_letters[g_char].add(i)
            elif f_char == self.BLACK:
                black_letters.add(g_char)

        for letter, positions in yellow_letters.items():
            if any(word[pos] == letter for pos in positions):
                return False

        if any(letter in word for letter in black_letters):
            return False

        return True

    def get_entropy(self, guess):
        """Calculates the entropy of a given guess."""
        pattern_counts = defaultdict(int)
        for word in self.possible_words:
            pattern = tuple(self.get_feedback(guess, word))
            pattern_counts[pattern] += 1

        entropy = 0
        total = len(self.possible_words)
        for count in pattern_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def get_optimal_guess(self):
        """Finds the optimal guess based on precomputed scores and entropy."""
        if not self.possible_words:
            return None

        max_score = -1
        best_guess = None
        for word in self.words:
            if word in self.possible_words:
                score = self.precomputed_scores[word] * 0.5 + self.get_entropy(word) * 0.5
            else:
                score = self.get_entropy(word) * 0.5
            if score > max_score:
                max_score = score
                best_guess = word

        return best_guess

    def get_feedback(self, guess, actual):
        """Generates feedback for a guess compared to the actual word."""
        feedback = []
        actual_letter_count = defaultdict(int)
        for char in actual:
            actual_letter_count[char] += 1

        for i, (g_char, a_char) in enumerate(zip(guess, actual)):
            if g_char == a_char:
                feedback.append(self.GREEN)
                actual_letter_count[g_char] -= 1
            else:
                feedback.append(None)

        for i, g_char in enumerate(guess):
            if feedback[i] is not None:
                continue
            if g_char in actual and actual_letter_count[g_char] > 0:
                feedback[i] = self.YELLOW
                actual_letter_count[g_char] -= 1
            else:
                feedback[i] = self.BLACK

        return feedback

    def reset(self):
        """Resets the possible words to the original list."""
        self.possible_words = self.words.copy()
