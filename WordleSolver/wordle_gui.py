# wordle_solver_gui.py

import tkinter as tk
from wordle_solver import WordleSolver


class WordleSolverGUI(tk.Tk):
    def __init__(self, solver):
        super().__init__()

        # Configure main window
        self.configure(bg='light grey')
        self.title('Wordle Solver')
        self.geometry('400x300')

        # Initialize solver and guesses
        self.solver = solver
        self.guesses = []

        # Define feedback color code
        self.feedback_colors = {'G': 'green', 'Y': 'yellow', 'B': 'dark grey'}

        # Initialize entry fields and feedback buttons
        self.entry_fields = self._initialize_entries()
        self.feedback_buttons = self._initialize_buttons()

        # Initialize submit button
        self._initialize_submit_button()

        # Initialize result and possible guesses labels
        self.result_label, self.possible_guesses_label = self._initialize_labels()

    def _initialize_entries(self):
        """Creates and places the entry fields in the window."""
        entries = []
        for i in range(5):
            entry = self._create_entry_field(i)
            entries.append(entry)
        return entries

    def _create_entry_field(self, index):
        """Creates a single entry field with the provided index."""
        entry_position = 50 + index * 70
        validate_command = self.register(self.limit_input_to_single_character)
        entry = tk.Entry(self, width=2, validate='key', validatecommand=(validate_command, '%P'))
        entry.config(font=('Helvetica', 24), justify='center', bg='dark grey')
        entry.bind('<Key>', lambda e, i=index: self.focus_on_next_entry(i))
        entry.place(x=entry_position, y=100)
        return entry

    def _initialize_buttons(self):
        """Creates and places the feedback buttons in the window."""
        buttons = []
        for i in range(5):
            button = self._create_feedback_button(i)
            buttons.append(button)
        return buttons

    def _create_feedback_button(self, index):
        """Creates a single feedback button with the provided index."""
        button_position = 50 + index * 70
        button = tk.Button(self, text='B', width=2, height=1, bg='dark grey')
        button.config(font=('Helvetica', 24))
        button.place(x=button_position, y=150)
        button.bind('<Button-1>', self.cycle_feedback_color)
        return button

    def _initialize_submit_button(self):
        """Creates and places the submit button in the window."""
        submit_button = tk.Button(self, text='Submit', command=self.submit_guess)
        submit_button.place(x=150, y=220)

    def _initialize_labels(self):
        """Creates and places the result and possible guesses labels in the window."""
        result_label = tk.Label(self, text='', bg='light grey')
        result_label.place(x=100, y=280)

        possible_guesses_label = tk.Label(self, text='', bg='light grey')
        possible_guesses_label.place(x=100, y=250)

        return result_label, possible_guesses_label

    def limit_input_to_single_character(self, input):
        """Ensure the input in the entry fields is only a single character."""
        return len(input) <= 1

    def focus_on_next_entry(self, index):
        """Focuses on the next entry field after a key press."""
        if index < 4:
            self.entry_fields[index + 1].focus()

    def submit_guess(self):
        """Submits the current guess and provides feedback."""
        guessed_word = ''.join(entry.get().lower() for entry in self.entry_fields)
        feedback = [button['text'] for button in self.feedback_buttons]
        self.solver.adjust_guess(guessed_word, feedback)
        optimal_guess = self.solver.get_optimal_guess()
        self.result_label['text'] = f'Optimal Guess: {optimal_guess}'
        self.guesses.append((guessed_word, feedback))

        # Reset entry fields and feedback buttons
        for entry, button in zip(self.entry_fields, self.feedback_buttons):
            entry.delete(0, tk.END)
            button['text'] = 'B'
            button['bg'] = 'dark grey'

        self.possible_guesses_label['text'] = f'Possible guesses remaining: {len(self.solver.possible_words)}'

    def cycle_feedback_color(self, event):
        """Cycles through feedback color options when the feedback button is clicked."""
        current_feedback = event.widget['text']
        feedback_values = list(self.feedback_colors.keys())
        new_feedback = feedback_values[(feedback_values.index(current_feedback) + 1) % len(feedback_values)]
        event.widget['text'] = new_feedback
        event.widget['bg'] = self.feedback_colors[new_feedback]


if __name__ == "__main__":
    # Instantiate the solver
    solver = WordleSolver('../frequencyMaps/validwords.txt',
                          '../frequencyMaps/word_freq_map.json',
                          '../frequencyMaps/letter_freq_map.json')

    # Create GUI and start the main loop
    solver_gui = WordleSolverGUI(solver)
    solver_gui.mainloop()