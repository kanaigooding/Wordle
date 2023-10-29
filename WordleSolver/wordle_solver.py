import json
import itertools


class WordleSolver:
    BLACK = 'B'  # Letter not in the word at all
    YELLOW = 'Y'  # Letter in the word but not in the right place
    GREEN = 'G'  # Letter in the correct place

    def __init__(self, valid_words_file, word_freq_file, letter_freq_file):
        self.words = self.load_words(valid_words_file)
        self.word_freq = self.load_freq(word_freq_file)
        self.letter_freq = self.load_freq(letter_freq_file)
        self.possible_words = self.words.copy()

    def load_words(self, file):
        try:
            with open(file, 'r') as f:
                words = f.read().splitlines()
            return words
        except FileNotFoundError:
            print(f"Error: File {file} not found!")
            return []

    def load_freq(self, file):
        try:
            with open(file, 'r') as f:
                freq = json.load(f)
            return freq
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error loading frequency from {file}!")
            return {}

    def adjust_guess(self, guessed_word, feedback):
        new_possible_words = [word for word in self.possible_words if self.is_possible(word, guessed_word, feedback)]
        self.possible_words = new_possible_words

    def is_possible(self, word, guessed_word, feedback):

        if word == guessed_word:
            return False

        for i in range(5):
            if feedback[i] == self.BLACK and guessed_word[i] in word:
                for x in range(i - 1):
                    if guessed_word[i] == guessed_word[x]:
                        feedback[i] = self.YELLOW
                return False
            if feedback[i] == self.YELLOW and guessed_word[i] == word[i]:
                return False
            if feedback[i] == self.YELLOW and guessed_word[i] not in word:
                return False
            if feedback[i] == self.GREEN and word[i] != guessed_word[i]:
                return False
        return True

    def get_optimal_guess(self):
        if not self.possible_words:
            return None

        print(self.possible_words)

        word_sum = sum(self.word_freq[word] for word in self.possible_words)

        def score_letter(word):
            return sum(self.letter_freq[letter] for letter in set(word))

        def word_score(word):
            return self.word_freq[word] / word_sum

        # First, check for any word with a word_score greater than 0.75
        for word in self.possible_words:
            if word_score(word) > 0.75:
                return word

        # If no such word is found, return the word with the highest score_letter
        return max(self.possible_words, key=score_letter)

    def get_most_eliminating_guess(self):
        if not self.possible_words:
            return None

        max_avg_eliminated = -1
        optimal_word = ''

        for word in self.possible_words:
            total_eliminated = sum(
                len(self.possible_words) - len([w for w in self.possible_words if self.is_possible(w, word, feedback)])
                for feedback in self.generate_all_possible_feedback()
            )

            avg_eliminated = total_eliminated / len(self.possible_words)

            if avg_eliminated > max_avg_eliminated:
                max_avg_eliminated = avg_eliminated
                optimal_word = word

        return optimal_word

    def generate_all_possible_feedback(self):
        return [''.join(x) for x in itertools.product([self.BLACK, self.YELLOW, self.GREEN], repeat=5)]

    def reset(self):
        self.possible_words = self.words.copy()
