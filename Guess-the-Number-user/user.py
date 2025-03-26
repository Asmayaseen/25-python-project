import random
import streamlit as st

def user_guess_game(x):
    random_number = random.randint(1, x)
    st.title('🎯 Guess the Number Game')
    st.write(f'Guess a number between 1 and {x}')

    guess = st.number_input('Enter your guess:', min_value=1, max_value=x, step=1)

    if guess < random_number:
        st.warning('📉 Too low! Try again.')
    elif guess > random_number:
        st.warning('📈 Too high! Try again.')
    else:
        st.success(f'🎉 Congratulations! You guessed the number {random_number} correctly.')

def computer_guess_game(x):
    low = 1
    high = x
    st.title('🖥️ Computer Guess the Number Game')
    st.write(f'Think of a number between 1 and {x}. The computer will try to guess it!')

    if low > high:
        st.error("Invalid range. Please restart the game.")
        return

    guess = random.randint(low, high)
    st.write(f'Computer guesses: {guess}')

    feedback = st.radio("Was the guess too high, too low, or correct?", ['Too High', 'Too Low', 'Correct'])

    if feedback == 'Too High':
        high = guess - 1
    elif feedback == 'Too Low':
        low = guess + 1
    else:
        st.success(f'🎉 Hurray! The computer guessed your number {guess} correctly.')
        return

    if low <= high:
        if st.button('Next Guess'):
            computer_guess_game(x)
    else:
        st.error('🤔 Something went wrong! Make sure your feedback is accurate.')

game_mode = st.radio('Choose Game Mode:', ['User Guesses the Number', 'Computer Guesses Your Number'])

if game_mode == 'User Guesses the Number':
    user_guess_game(10)
else:
    computer_guess_game(10)