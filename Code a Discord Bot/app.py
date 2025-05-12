import streamlit as st # type: ignore
import subprocess
import os

def write_env_variable(token):
    with open(".env", "w") as f:
        f.write(f"DISCORD_BOT_TOKEN={token}")

def run_bot():
    st.session_state.process = subprocess.Popen(["python", "bot.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    st.session_state.running = True

def stop_bot():
    if hasattr(st.session_state, 'process') and st.session_state.process:
        st.session_state.process.terminate()
        st.session_state.running = False

# Streamlit UI
st.title('🤖 Discord Bot Manager')
st.write('Start or stop your Discord bot using this interface.')

bot_token = st.text_input("Enter your Discord Bot Token:", type="password")

if st.button("Save Token"):
    if bot_token.strip():
        write_env_variable(bot_token)
        st.success("Token saved successfully!")
    else:
        st.error("Token cannot be empty!")

if st.button("Start Bot"):
    if bot_token.strip():
        run_bot()
        st.success("Bot started!")
    else:
        st.error("Please enter a valid token.")

if st.button("Stop Bot"):
    stop_bot()
    st.warning("Bot stopped!")

if st.session_state.get('running', False):
    st.info("Bot is running...")

st.markdown("<div style='text-align: center; margin-top: 30px;'>Made with ❤️ by Asma Yaseen</div>", unsafe_allow_html=True)
