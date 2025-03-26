import streamlit as st # type: ignore
import pandas as pd # type: ignore
import random
import time
from datetime import datetime

# ✅ Page Configuration
st.set_page_config(page_title="🌿 Calm Companion", layout='wide', initial_sidebar_state="expanded")

# 🔄 Initialize session state
st.session_state.setdefault("dark_mode", False)

# 🌙 Dark Mode Toggle
dark_mode = st.sidebar.toggle("🌙 Night Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# 🌿 Custom Styling for Light and Dark Mode
base_styles = f"""
    <style>
        .title {{ text-align: center; font-size: 32px; font-weight: bold; color: {'#4CAF50' if not dark_mode else '#BB86FC'}; }}
        .card {{ padding: 20px; border-radius: 12px; margin-bottom: 20px; background-color: {'#FAFAFA' if not dark_mode else '#2E2E2E'}; color: {'black' if not dark_mode else 'white'}; }}
        body {{ background-color: {'#FFFFFF' if not dark_mode else '#121212'}; color: {'black' if not dark_mode else 'white'}; }}
        .stButton button, .stDownloadButton button {{ background-color: {'#4CAF50' if not dark_mode else '#BB86FC'}; color: white; border-radius: 8px; }}
    </style>
"""
st.markdown(base_styles, unsafe_allow_html=True)

# 🎯 Header
st.markdown('<h1 class="title">🌿 Calm Companion: Your Daily Reflection</h1>', unsafe_allow_html=True)
st.write("Pause, reflect, and embrace moments of mindfulness every day.")

# ✅ Sidebar - Profile
st.sidebar.header("🧑 Your Reflection")
name = st.sidebar.text_input("What's your name?", placeholder="Enter your name")
current_date = datetime.now().strftime('%Y-%m-%d')

# 🌟 Daily Affirmation
affirmations = [
    "I welcome calm into my life.",
    "I am resilient and grounded.",
    "I embrace peace and gratitude.",
    "I choose to respond with patience.",
    "Every breath I take brings me peace.",
]
st.sidebar.subheader("🌻 Your Daily Affirmation")
st.sidebar.write(f"✨ *{random.choice(affirmations)}*")

# 🎭 Mood Tracker
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌈 How are you feeling today?")
moods = ["Joyful", "Serene", "Anxious", "Overwhelmed", "Fatigued", "Motivated"]
selected_mood = st.radio("Select your mood:", moods, horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# 🌼 Gratitude Journal
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌼 Gratitude Journal")
gr1 = st.text_input("🌿 Something I’m thankful for:", placeholder="Write here...")
gr2 = st.text_input("🌿 Another blessing I appreciate:", placeholder="Write here...")
gr3 = st.text_input("🌿 One more reason to smile today:", placeholder="Write here...")
st.markdown('</div>', unsafe_allow_html=True)

# 🌿 Mindfulness Challenge
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌿 Mindful Action of the Day")
challenges = [
    "Breathe deeply for 5 minutes.",
    "Write down 3 things that made you smile today.",
    "Step outside and enjoy the fresh air.",
    "Listen to your favorite calming music.",
    "Practice a short body scan meditation.",
]
st.write(f"💭 Today's Activity: *{random.choice(challenges)}*")
st.markdown('</div>', unsafe_allow_html=True)

# 🌬 Breathing Exercise
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🫧 Relax with a Breathing Exercise")
breath_time = st.slider("Set your breathing time (seconds):", 10, 60, 30)
if st.button("🕊 Start Breathing Session"):
    st.success("🌿 Inhale... Hold... Exhale... Relax...")
    time.sleep(breath_time)
    st.info("💆‍♀️ Great job! Take a moment to enjoy your calm state.")
st.markdown('</div>', unsafe_allow_html=True)

# 📊 Save & Display Progress
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Track Your Progress")
if st.button("💾 Save Today's Reflection"):
    data = pd.DataFrame({
        "Name": [name if name else "Anonymous"],
        "Date": [current_date],
        "Mood": [selected_mood],
        "Gratitude 1": [gr1],
        "Gratitude 2": [gr2],
        "Gratitude 3": [gr3],
    })
    st.success("✅ Your reflection has been saved! Keep embracing mindful moments.")
    st.dataframe(data)

    # 📥 Download Data
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Reflection Log",
        data=csv,
        file_name=f"calm_companion_{name}_{current_date}.csv",
        mime="text/csv",
    )
st.markdown('</div>', unsafe_allow_html=True)

# 📊 Mood Trend Chart
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Mood Tracker Overview")
chart_data = pd.DataFrame(
    {"Mood": moods, "Occurrences": [2, 5, 3, 1, 4, 6]}
)
st.bar_chart(chart_data)
st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.write("🌸 Stay mindful, stay calm. You deserve peace and joy! 🕊")
