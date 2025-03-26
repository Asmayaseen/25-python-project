import random
import streamlit as st # type: ignore

def is_win(player, opponent):
    # r > s, s > p, p > r
    return (player == 'r' and opponent == 's') or (player == 's' and opponent == 'p') or (player == 'p' and opponent == 'r')

def play(user_choice):
    computer_choice = random.choice(['r', 'p', 's'])

    st.write(f"You chose: {user_choice}")
    st.write(f"Computer chose: {computer_choice}")

    if user_choice == computer_choice:
        return "It's a tie!"

    if is_win(user_choice, computer_choice):
        return "You won! 🎉"

    return "You lost! 😢"

# Streamlit UI
st.title('Rock, Paper, Scissors Game')
st.write("Choose one:")

user_choice = st.radio("Select your choice:", ('r - Rock', 'p - Paper', 's - Scissors'))
user_choice = user_choice[0]  # Extracting 'r', 'p', or 's'

if st.button('Play'): 
    result = play(user_choice)
    st.write(result)

st.write("---")
st.write("'r' for Rock, 'p' for Paper, 's' for Scissors")
