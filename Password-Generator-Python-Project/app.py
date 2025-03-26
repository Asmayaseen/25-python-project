import streamlit as st # type: ignore
import random
import string

# Emoji collections
emoji_list = ['😀', '😎', '🤖', '🐱', '🐶', '🌵', '🍕', '🚀', '💡', '🎵', '📚', '🧡', '🌟', '🍩', '🦄', '🥳', '🌈']

# Password generation function
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    emoji_password = ''.join(random.choice(emoji_list) for _ in range(3)) + password + ''.join(random.choice(emoji_list) for _ in range(3))
    return emoji_password

# Streamlit UI
st.title('🔐 Password Generator')

num_passwords = st.number_input('How many passwords do you want to generate?', min_value=1, max_value=20, value=5)
password_length = st.slider('Select the password length:', min_value=8, max_value=24, value=12)

if st.button('Generate Passwords 🚀'):
    st.write('## Your Passwords:')
    for i in range(num_passwords):
        password = generate_password(password_length)
        st.write(f'🔑 **Password {i+1}**: {password}')

st.write('💡 Tip: Copy your favorite password and store it securely!')
