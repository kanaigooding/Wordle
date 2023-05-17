# wordle_gui.py

import tkinter as tk
from wordle_solver import WordleSolver

class WordleGUI(tk.Tk):
    def __init__(self, solver):
        super().__init__()
        self.title('Wordle Solver')
        self.geometry('400x300')
        self.solver = solver
        self.guesses = []
        self.guess_entry_fields = []
        self.guess_feedback_fields = []
        self.feedback_colors = {'G': 'green', 'Y': 'yellow', 'B': 'black'}

        for i in range(5):
            validate_command = self.register(self.limit_characters)
            guess_entry = tk.Entry(self, width=2, validate='key', validatecommand=(validate_command, '%P'))
            guess_entry.bind('<Key>', lambda e, i=i: self.focus_next(i))
            guess_entry.place(x=100 + i*50, y=100)  # adjust placement
            self.guess_entry_fields.append(guess_entry)

        for i in range(5):
            feedback_field = tk.Button(self, text='B', width=2)
            feedback_field.place(x=100 + i*50, y=150)  # adjust placement
            feedback_field.bind('<Button-1>', self.cycle_feedback)
            self.guess_feedback_fields.append(feedback_field)

        submit_button = tk.Button(self, text='Submit', command=self.submit)
        submit_button.place(x=175, y=200)  # centered placement

        result_label = tk.Label(self, text='')
        result_label.place(x=100, y=250)  # centered placement
        self.result_label = result_label

    def limit_characters(self, input):
        return len(input) <= 1

    def focus_next(self, index):
        if index < 4:
            self.guess_entry_fields[index+1].focus()

    def submit(self):
        guessed_word = ''.join(entry.get().lower() for entry in self.guess_entry_fields)
        feedback = [field['text'] for field in self.guess_feedback_fields]
        self.solver.adjust_guess(guessed_word, feedback)
        optimal_guess = self.solver.get_optimal_guess()
        self.result_label['text'] = f'Optimal Guess: {optimal_guess}'
        self.guesses.append((guessed_word, feedback))

    def cycle_feedback(self, event):
        current_feedback = event.widget['text']
        feedback_values = list(self.feedback_colors.keys())
        new_feedback = feedback_values[(feedback_values.index(current_feedback) + 1) % len(feedback_values)]
        event.widget['text'] = new_feedback
        event.widget['bg'] = self.feedback_colors[new_feedback]

if __name__ == "__main__":
    solver = WordleSolver('validwords.txt', 'word_freq_map.json', 'letter_freq_map.json')
    gui = WordleGUI(solver)
    gui.mainloop()
