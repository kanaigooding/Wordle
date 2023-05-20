import json

class WordleSolver:
    """
    A class to encapsulate a Wordle game solver.
    """

    def __init__(self, valid_words_file, word_freq_file, letter_freq_file):
        # Load the valid words, word frequencies and letter frequencies at initialization
        self.words = self._load_words(valid_words_file)
        self.word_freq = self._load_freq(word_freq_file)
        self.letter_freq = self._load_freq(letter_freq_file)
        self.possible_words = self.words.copy()

    def _load_words(self, file):
        """
        Load words from a file. Assumes one word per line.
        """
        with open(file, 'r') as f:
            words = f.read().splitlines()
        return words

    def _load_freq(self, file):
        """
        Load frequencies (word or letter) from a file. Assumes file is in JSON format.
        """
        with open(file, 'r') as f:
            freq = json.load(f)
        return freq

    def adjust_guess(self, guessed_word, feedback):
        """
        Given a word and feedback, adjust the list of possible words.
        """
        new_possible_words = [word for word in self.possible_words if self._is_possible(word, guessed_word, feedback)]
        self.possible_words = new_possible_words

    def _is_possible(self, word, guessed_word, feedback):
        """
        Check if a word is a possible solution given a guessed word and feedback.
        """
        for i in range(5):
            if ((feedback[i] == 'G' and word[i] != guessed_word[i]) or
                (feedback[i] == 'B' and word[i] == guessed_word[i]) or
                (feedback[i] == 'Y' and (guessed_word[i] == word[i] or not word.__contains__(guessed_word[i])))):
                return False
        return True

    def get_optimal_guess(self):
        """
        Get the most optimal guess from the list of possible words.
        If there are no possible words left, return a message.
        """
        if not self.possible_words:
            return "No optimal guess could be made."

        # Select the word with the highest score as the optimal guess
        optimal_word = max(self.possible_words, key=self._get_word_score)
        return optimal_word

    def _get_word_score(self, word):
        """
        Calculate the score of a word, considering both the word frequency and letter frequencies.
        """
        word_score = self.word_freq.get(word, 0)
        letter_score = sum(self.letter_freq.get(letter, 0) for letter in word)
        return word_score + letter_score

    def reset(self):
        """
        Reset the solver to the initial state.
        """
        self.possible_words = self.words.copy()
