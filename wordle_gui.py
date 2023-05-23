# wordle_gui.py

import tkinter as tk
from wordle_solver import WordleSolver


class WordleGUI(tk.Tk):
    def __init__(self, solver):
        super().__init__()
        self.configure(bg='light grey')
        self.title('Wordle Solver')
        self.geometry('400x300')
        self.solver = solver
        self.guesses = []
        self.feedback_colors = {'G': 'green', 'Y': 'yellow', 'B': 'dark grey'}

        self.entries = []
        for i in range(5):
            validate_command = self.register(self.limit_characters)
            entry = tk.Entry(self, width=2, validate='key', validatecommand=(validate_command, '%P'))
            entry.config(font=('Helvetica', 24), justify='center', bg='dark grey')
            entry.bind('<Key>', lambda e, i=i: self.focus_next(i))
            entry.place(x=50 + i * 70, y=100)  # adjust placement
            self.entries.append(entry)

        self.feedback_buttons = []
        for i in range(5):
            button = tk.Button(self, text='B', width=2, height=1, bg='dark grey')
            button.config(font=('Helvetica', 24))
            button.place(x=50 + i * 70, y=150)  # adjust placement
            button.bind('<Button-1>', self.cycle_feedback)
            self.feedback_buttons.append(button)

        submit_button = tk.Button(self, text='Submit', command=self.submit)
        submit_button.place(x=150, y=220)  # centered placement

        self.result_label = tk.Label(self, text='', bg='light grey')
        self.result_label.place(x=100, y=280)  # centered placement

        self.previous_guesses_label = tk.Label(self, text='Previous Guesses:', bg='light grey')
        self.previous_guesses_label.place(x=20, y=320)

        self.previous_guesses_text = tk.Text(self, height=5, width=20)
        self.previous_guesses_text.place(x=20, y=350)

    @staticmethod
    def limit_characters(input):
        return len(input) <= 1

    def focus_next(self, index):
        if index < 4:
            self.entries[index + 1].focus()

    def submit(self):
        guessed_word = ''.join(entry.get().lower() for entry in self.entries)
        feedback = [button['text'] for button in self.feedback_buttons]
        self.solver.adjust_guess(guessed_word, feedback)
        optimal_guess = self.solver.get_optimal_guess()
        self.result_label['text'] = f'Optimal Guess: {optimal_guess}'
        self.guesses.append((guessed_word, feedback))

        # reset entries and feedback buttons
        for entry, button in zip(self.entries, self.feedback_buttons):
            entry.delete(0, tk.END)
            button['text'] = 'B'
            button['bg'] = 'dark grey'

        # update previous guesses
        self.previous_guesses_text.insert(tk.END, f'{guessed_word} {feedback}\n')

    def cycle_feedback(self, event):
        current_feedback = event.widget['text']
        feedback_values = list(self.feedback_colors.keys())
        new_feedback = feedback_values[(feedback_values.index(current_feedback) + 1) % len(feedback_values)]
        event.widget['text'] = new_feedback
        event.widget['bg'] = self.feedback_colors[new_feedback]


if __name__ == "__main__":
    solver = WordleSolver('frequencyMaps/validwords.txt', 'frequencyMaps/word_freq_map.json', 'frequencyMaps/letter_freq_map.json')
    gui = WordleGUI(solver)
    gui.mainloop()
