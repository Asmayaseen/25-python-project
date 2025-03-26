import streamlit as st
import random
import re
from collections import defaultdict

st.set_page_config(page_title="Markov Chain Text Composer 🎵", page_icon="🎶")
st.title("Markov Chain Text Composer 🎵✨")
st.write("Generate random text using the Markov Chain model!")

# Process text into Markov Chain model
def build_markov_chain(text, n=2):
    words = re.findall(r"\b\w+\b", text.lower())
    markov_chain = defaultdict(list)

    for i in range(len(words) - n):
        key = tuple(words[i:i+n])
        next_word = words[i+n]
        markov_chain[key].append(next_word)

    return markov_chain

# Generate text using Markov Chain
def generate_text(chain, start_words):
    if start_words not in chain:
        return "Invalid starting words. Try different ones."
    result = list(start_words)

    while True:
        next_words = chain.get(start_words, None)
        if not next_words:
            break
        next_word = random.choice(next_words)
        result.append(next_word)
        start_words = tuple(result[-len(start_words):])

    return " ".join(result)

# Input text
uploaded_file = st.file_uploader("Upload a text file (.txt) for training the Markov model", type="txt")

if uploaded_file is not None:
    text_data = uploaded_file.read().decode('utf-8')
    st.success("Text file uploaded successfully! 📚")

    # Build Markov Chain
    chain = build_markov_chain(text_data)
    st.sidebar.info(f"Markov Chain Model built with {len(chain)} unique states.")

    # Generate Lyrics Button
    if st.button("Generate Lyrics 🎵"):
        random_start = random.choice(list(chain.keys()))
        generated_text = generate_text(chain, random_start)
        st.write("### Generated Lyrics:")
        st.write(generated_text)

    # Reset Button
    if st.button("Reset 🔄"):
        st.rerun()

st.sidebar.info("Developed with 💖 using Streamlit and Markov Chains by Asma Yaseen")
