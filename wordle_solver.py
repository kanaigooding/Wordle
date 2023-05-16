# wordle_solver.py

class WordleSolver:
    def __init__(self, valid_words_file):
        self.words = self.load_words(valid_words_file)
        self.possible_words = self.words.copy()

    def load_words(self, file):
        with open(file, 'r') as f:
            words = f.read().splitlines()
        return words

    def adjust_guess(self, guess):
        new_possible_words = []
        for word in self.possible_words:
            if self.is_possible(word, guess):
                new_possible_words.append(word)
        self.possible_words = new_possible_words

    def is_possible(self, word, guess):
        for i in range(5):
            if guess[i] == 'G' and word[i] != guess[i]:
                print("G")
                return False
            if guess[i] == 'B' and word[i] == guess[i]:
                print("B")
                return False
            if guess[i] == 'Y' and (word[i] == guess[i] or word.count(guess[i]) == 0):
                print("Y")
                return False
        return True

    def get_optimal_guess(self):
        if self.possible_words:
            return self.possible_words[0]
        else:
            return "No optimal guess could be made."

    def reset(self):
        self.possible_words = self.words.copy()


if __name__ == "__main__":
    solver = WordleSolver('validwords.txt')
    print(solver.get_optimal_guess())  # Should print the first word in 'validwords.txt'
    solver.adjust_guess('BBBBB')  # Should remove all words that have a correct letter from 'possible_words'
    print(
        solver.get_optimal_guess())  # Should print the first word in 'possible_words' that doesn't contain a correct letter
