import requests
import random
import string
import time

# API URL
BASE_URL = "https://wordle.votee.dev:8000"
WORD_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

# Load a list of valid five-letter English words (first time load from GitHub only)
def load_valid_words():
    url = WORD_URL
    response = requests.get(url)
    all_words = response.text.splitlines()
    return [word.lower() for word in all_words if len(word) == 5]

VALID_WORDS = load_valid_words()

#Initial guesses use high frequency vowel combinations
def select_initial_guess():
    return random.choice(VALID_WORDS)

# Send a guess request
def make_guess(guess, word=None, mode="daily",seed=None):
    if mode == "word" and word:
        url = f"{BASE_URL}/word/{word}"
        response = requests.get(url, params={"guess": guess})
    elif mode == "random":
        url = f"{BASE_URL}/random"
        response = requests.get(url, params={"guess": guess,"seed":seed})
    elif mode == "daily":
        url = f"{BASE_URL}/daily"
        response = requests.get(url, params={"guess": guess})
    else:
        print(f"wrong mode: {mode}.please use 'word'、'random' or 'daily'。")
        return None

    if response.status_code == 200:
        return response.json()
    else:
        print(f"request error：{response.json()}")
        return None

# Main game logic
def play_game(mode="daily", word=None, rounds=1):
    word_length = 5
    print(f"game mode：{mode}")

    for round in range(rounds):
        print(f"======= Round {round + 1} =======")
        guess = select_initial_guess()
        print(f"Initial guess: {guess}")

        # Use the round number as a seed to ensure consistency in each round of the game
        seed = round  
        result = make_guess(guess, word=word, mode=mode, seed=seed)
        
        if result:
            process_result(guess, result)

        correct_letters = [None] * word_length
        present_letters = set()
        absent_letters = set()
        present_wrong_positions = {}

        attempts = 0
        while result and attempts < 6:
            attempts += 1
            print(f"Attempt {attempts} ...")

            correct_letters, present_letters, absent_letters, present_wrong_positions = update_known_letters(
                correct_letters, present_letters, absent_letters, present_wrong_positions, result, guess)

            guess = generate_guess(correct_letters, present_letters, absent_letters, present_wrong_positions)
            if not guess:
                print("Unable to find a valid word.")
                break

            print(f"New guess: {guess}")
            result = make_guess(guess, word=word, mode=mode, seed=seed)

            if result:
                process_result(guess, result)

                if all(item['result'] == 'correct' for item in result):
                    print("Congrets，all letters guess correctly，game over！")
                    break

            time.sleep(1)

        print("game over.")

# Output return result
def process_result(guess, result):
    print(f"Guess: {guess} - result:")
    for item in result:
        print(f"position {item['slot']}: letter '{item['guess']}' - status: {item['result']}")

# Update known information is used to update known information based on the results of the current guess so that some invalid options can be eliminated more accurately during the next guess.
def update_known_letters(correct_letters, present_letters, absent_letters, present_wrong_positions, result, guess):
    for i, item in enumerate(result):
        letter = item['guess']
        status = item['result']

         
        if status == "correct":
            correct_letters[i] = letter
            
        elif status == "present":
            present_letters.add(letter)
            if letter not in present_wrong_positions:
                present_wrong_positions[letter] = set()
            present_wrong_positions[letter].add(i)
        elif status == "absent":
            if letter not in correct_letters and letter not in present_letters:
                absent_letters.add(letter)

    return correct_letters, present_letters, absent_letters, present_wrong_positions

# Generate new guesses (select from the vocabulary) based on known information. The method is to filter out qualified words from the legal word list based on the currently known letter information (correct letters, letters in the wrong position, missing letters, etc.), and then randomly select one as the new guess.
def generate_guess(correct_letters, present_letters, absent_letters, present_wrong_positions):
    candidates = []

    for word in VALID_WORDS:
        # Check if the correct letters match
        if any(c is not None and word[i] != c for i, c in enumerate(correct_letters)):
            continue

        # Check if the absent letter exists
        if any(letter in absent_letters for letter in word):
            continue

        # Check if present contains all letters
        if not present_letters.issubset(set(word)):
            continue

        # Check that the present letter does not appear in the wrong position
        if any(word[i] in present_wrong_positions and i in present_wrong_positions[word[i]] for i in range(5)):
            continue

        candidates.append(word)

    return random.choice(candidates) if candidates else None

# Program entry
if __name__ == "__main__":
    mode = "daily"  # "random", "daily", "word"

    # If in guess mode, provide the test word; otherwise set to None
    test_word = "hello" if mode == "word" else None

    play_game(mode, test_word)
