import random
import streamlit as st # type: ignore

def user_guess(x):
    random_number = random.randint(1, x)
    guess = 0
    st.write(f"🎯 Guess a number between 1 and {x}!")

    user_guess = st.number_input("🔢 Enter your guess:", min_value=1, max_value=x, step=1, key='user_guess')

    if st.button('🚀 Submit Guess', key='submit_guess'):
        if user_guess < random_number:
            st.warning('📉 Too low. Guess again!')
        elif user_guess > random_number:
            st.warning('📈 Too high. Guess again!')
        else:
            st.success(f'🎉 Yay, congrats! You guessed the number {random_number} correctly! 🎊')

def computer_guess(x):
    low = 1
    high = x
    guess = random.randint(low, high)

    st.write(f"🤖 Think of a number between 1 and {x}, and the computer will guess it!")
    st.write(f"💡 Computer guesses: {guess}")

    feedback = st.radio("📢 Was the guess too high, too low, or correct?", ['Too High', 'Too Low', 'Correct'], key=f"radio_feedback_{guess}")

    if feedback == 'Correct':
        st.success(f'🎊 Yay! The computer guessed your number {guess} correctly! 🎉')
    else:
        if feedback == 'Too High':
            high = guess - 1
        elif feedback == 'Too Low':
            low = guess + 1

        if low <= high:
            st.button('🔎 Next Guess', key=f'next_guess_{guess}', on_click=lambda: computer_guess(x))
        else:
            st.error('🚫 Something went wrong! Please restart the game.')

# Streamlit UI
st.title('🎮 Guess The Number Game')
mode = st.radio('🕹️ Choose Game Mode:', ['User Guesses the Number', 'Computer Guesses Your Number'], key='mode_selection')

if mode == 'User Guesses the Number':
    user_guess(10)
else:
    computer_guess(10)