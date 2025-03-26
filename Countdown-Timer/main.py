import streamlit as st
import time

# Streamlit app configuration
st.set_page_config(page_title="Countdown Timer", layout="centered")
st.title("🕰 Countdown Timer with Stop & Resume")

# Dark and Light Mode using Streamlit themes
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"

def switch_theme():
    st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"

# Theme Toggle Button
st.button(f"Switch to {'Dark' if st.session_state.theme == 'Light' else 'Light'} Mode", on_click=switch_theme)

# Apply Theme Colors
if st.session_state.theme == "Dark":
    st.markdown(
        """<style>
        body {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        </style>""", unsafe_allow_html=True
    )
else:
    st.markdown(
        """<style>
        body {
            background-color: #f0f2f6;
            color: #000000;
        }
        .stButton>button {
            background-color: #008CBA;
            color: white;
        }
        </style>""", unsafe_allow_html=True
    )

# Initialize session state variables
if "running" not in st.session_state:
    st.session_state.running = False
if "time_left" not in st.session_state:
    st.session_state.time_left = 0
if "paused_at" not in st.session_state:
    st.session_state.paused_at = None
if "initial_time" not in st.session_state:
    st.session_state.initial_time = 10

# Input for countdown time
seconds = st.number_input("⏲ Enter countdown time (seconds):", min_value=1, step=1, value=st.session_state.initial_time)

# Layout for buttons
col1, col2, col3, col4 = st.columns(4)
start_btn = col1.button("🚀 Start")
stop_btn = col2.button("🛑 Stop")
resume_btn = col3.button("⏯ Resume")
clear_btn = col4.button("🔁 Reset")

# Start Timer
if start_btn:
    st.session_state.time_left = int(seconds)
    st.session_state.initial_time = int(seconds)
    st.session_state.running = True
    st.session_state.start_time = time.time()
    st.session_state.paused_at = None

# Stop Timer
if stop_btn and st.session_state.running:
    elapsed_time = time.time() - st.session_state.start_time
    st.session_state.time_left = max(0, st.session_state.time_left - int(elapsed_time))
    st.session_state.running = False
    st.session_state.paused_at = st.session_state.time_left

# Resume Timer
if resume_btn and st.session_state.paused_at is not None:
    st.session_state.running = True
    st.session_state.start_time = time.time()
    st.session_state.time_left = st.session_state.paused_at
    st.session_state.paused_at = None

# Clear Timer
if clear_btn:
    st.session_state.running = False
    st.session_state.time_left = 0
    st.session_state.paused_at = None
    st.session_state.initial_time = 10
    st.rerun()

# Display Timer with dynamic updates
if st.session_state.running and st.session_state.time_left > 0:
    countdown_placeholder = st.empty()

    while st.session_state.time_left > 0 and st.session_state.running:
        elapsed_time = int(time.time() - st.session_state.start_time)
        remaining_time = max(0, st.session_state.time_left - elapsed_time)

        mins, secs = divmod(remaining_time, 60)
        countdown_placeholder.subheader(f"⏳ {mins:02}:{secs:02}")

        if remaining_time == 0:
            st.success("🎉 Time's Up!")
            st.session_state.running = False
            break

        time.sleep(1)
        st.rerun()

# Display Paused Time
if not st.session_state.running and st.session_state.paused_at is not None:
    mins, secs = divmod(st.session_state.paused_at, 60)
    st.subheader(f"⏸ {mins:02}:{secs:02} (Paused)")

# Footer
st.markdown("---")
st.markdown("💻 **Developed by Asma Yaseen** 🌟")