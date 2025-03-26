import random
from words import words
from hangman_visual import lives_visual_dict
import string
import streamlit as st

def get_valid_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()

def hangman():
    if 'word' not in st.session_state:
        st.session_state.word = get_valid_word(words)
        st.session_state.word_letters = set(st.session_state.word)
        st.session_state.alphabet = set(string.ascii_uppercase)
        st.session_state.used_letters = set()
        st.session_state.lives = 7

    st.title("Hangman Game")
    st.write(f"You have {st.session_state.lives} lives left.")
    st.write("Used Letters: " + " ".join(st.session_state.used_letters))
    
    # Display the visual
    st.text(lives_visual_dict[st.session_state.lives])

    # Show current word with guesses
    word_list = [letter if letter in st.session_state.used_letters else '-' for letter in st.session_state.word]
    st.write("Current Word: " + " ".join(word_list))

    # Get user input
    user_letter = st.text_input("Guess a letter:").upper()

    if user_letter and user_letter in st.session_state.alphabet - st.session_state.used_letters:
        st.session_state.used_letters.add(user_letter)
        if user_letter in st.session_state.word_letters:
            st.session_state.word_letters.remove(user_letter)
            st.success("Good guess!")
        else:
            st.session_state.lives -= 1
            st.error(f"Wrong guess! {user_letter} is not in the word.")
    elif user_letter in st.session_state.used_letters:
        st.warning("You already guessed that letter!")
    elif user_letter:
        st.error("Invalid input. Please enter a valid letter.")

    # Game over scenarios
    if st.session_state.lives == 0:
        st.text(lives_visual_dict[0])
        st.error(f"You died! The word was {st.session_state.word}")
        st.button("Restart", on_click=reset_game)
    elif len(st.session_state.word_letters) == 0:
        st.success(f"Congratulations! You guessed the word {st.session_state.word}!!")
        st.button("Play Again", on_click=reset_game)

def reset_game():
    st.session_state.clear()

if __name__ == "__main__":
    hangman()
