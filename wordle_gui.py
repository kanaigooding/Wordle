# wordle_gui.py

import tkinter as tk

from wordle_solver import WordleSolver


class WordleGUI:
    def __init__(self, solver):
        self.solver = solver
        self.root = tk.Tk()
        self.root.title("Wordle Solver")

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack()

        self.entry = tk.Entry(self.input_frame)
        self.entry.pack()

        self.submit_button = tk.Button(self.input_frame, text="Submit Guess", command=self.submit_guess)
        self.submit_button.pack()

        self.reset_button = tk.Button(self.input_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.pack()

        self.label = tk.Label(self.output_frame, text="Enter your guesses to get the next optimal guess.")
        self.label.pack()

    def submit_guess(self):
        guess = self.entry.get().upper()
        self.solver.adjust_guess(guess)
        optimal_guess = self.solver.get_optimal_guess()
        self.label.config(text=f"Optimal guess: {optimal_guess}")
        self.entry.delete(0, 'end')

    def reset_game(self):
        self.solver.reset()
        self.label.config(text="Enter your guesses to get the next optimal guess.")
        self.entry.delete(0, 'end')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    solver = WordleSolver('validwords.txt')
    gui = WordleGUI(solver)
    gui.run()
