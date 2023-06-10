# quordle_solver.py

import json


class QuordleSolver:
    def __init__(self, valid_words_file, word_freq_file, letter_freq_file):
        self.words = self.load_words(valid_words_file)
        self.word_freq = self.load_freq(word_freq_file)
        self.letter_freq = self.load_freq(letter_freq_file)
        self.possible_words = [self.words.copy() for _ in range(4)]

    def load_words(self, file):
        with open(file, 'r') as f:
            words = f.read().splitlines()
        return words

    def load_freq(self, file):
        with open(file, 'r') as f:
            freq = json.load(f)
        return freq

    def adjust_guesses(self, guessed_words, feedbacks):
        for i in range(4):
            new_possible_words = []
            for word in self.possible_words[i]:
                if self.is_possible(word, guessed_words[i], feedbacks[i]):
                    new_possible_words.append(word)
            self.possible_words[i] = new_possible_words

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

    def get_possibilities_count(self):
        return [len(words) for words in self.possible_words]

    def get_optimal_guesses(self):
        optimal_guesses = []
        for i in range(4):
            if not self.possible_words[i]:
                optimal_guesses.append((None, 0))
                continue

            max_score = -1
            total_word_score = sum(self.word_freq.get(word, 0) for word in self.possible_words[i])
            optimal_word = ''

            for word in self.possible_words[i]:
                word_score = self.get_word_score(word, total_word_score)
                if word_score > max_score:
                    max_score = word_score
                    optimal_word = word

            optimal_guesses.append((optimal_word, len(self.possible_words[i])))

        return optimal_guesses

    def get_word_score(self, word, total_word_score):
        word_score = self.word_freq.get(word, 0) / total_word_score
        letter_score = 0
        for letter in set(word):
            letter_score += self.letter_freq.get(letter.lower(), 1)
        return letter_score

    def reset(self):
        self.possible_words = [self.words.copy() for _ in range(4)]
