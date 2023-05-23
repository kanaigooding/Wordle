# Wordle Solver

Wordle Solver is a Python-based application that assists in finding the optimal word in the Wordle game, which has become increasingly popular. The solver uses frequency maps for words and letters to suggest the most likely word based on your previous guesses and the game's feedback.

## Features

- User-friendly Graphical User Interface (GUI)
- Uses word and letter frequency maps to suggest the most probable words
- Adjusts possible word list based on the feedback of your guesses
- Easy to use, allowing users to focus more on the game

## Requirements

- Python 3.7 or higher
- Tkinter library for Python
- JSON data files for word and letter frequency maps (provided)

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/kanaigooding/wordle-solver.git
```

2. Install the required libraries:

```bash
pip install -r requirements.txt
```

3. Run the wordle_gui.py script to start the application:

```bash
python wordle_gui.py
```

## Usage

1. Start the application
2. In the GUI, enter your guessed word
3. Indicate the feedback from the game by clicking on the buttons below each letter. They will cycle through 'G', 'Y', and 'B' colors.
4. Submit your guess and feedback by clicking on the 'Submit' button.
5. The solver will suggest an optimal word, which will be displayed on the GUI.
6. Repeat the process until you've guessed the correct word.

## Contribute

Your contributions are always welcome! Please create a pull request to contribute to this project.

## License

This project is licensed under [MIT License](LICENSE).

---