# Wordle Game AI Helper

This project is an AI assistant for solving Wordle puzzles. It interacts with the Wordle API to make guesses and refine its strategy across multiple rounds. The assistant supports three modes: **random**, **word**, and **daily**.

## Features

- **Random Mode**: Solves randomly generated Wordle puzzles using a custom seed.
- **Word Mode**: Solves puzzles when the target word is known in advance.
- **Daily Mode**: Solves the current day's Wordle challenge.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/WaimanTsang/wordle
   cd wordle

2.Install the necessary dependencies

## Usage
1.Set the mode variable in the script to one of the following options:

"daily": Play today's Wordle puzzle.

"random": Solve a random Wordle puzzle using a custom seed.

"word": Solve a puzzle where the target word is known in advance (for testing).

2.Run the game:
python main.py

Example

mode = "daily"  # Set mode to "daily", "random", or "word"
test_word = "hello" if mode == "word" else None  # Provide a target word for "word" mode

play_game(mode, test_word)


