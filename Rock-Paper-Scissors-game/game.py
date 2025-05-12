import random
import streamlit as st

# Emoji mapping for choices
CHOICE_EMOJIS = {
    'r': '🪨 Rock',
    'p': '📄 Paper',
    's': '✂️ Scissors'
}

# Reverse mapping for radio button selection
RADIO_OPTIONS = {
    '🪨 Rock': 'r',
    '📄 Paper': 'p',
    '✂️ Scissors': 's'
}

# Game logic
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    if (user_choice == 'r' and computer_choice == 's') or \
       (user_choice == 's' and computer_choice == 'p') or \
       (user_choice == 'p' and computer_choice == 'r'):
        return "user"
    return "computer"

# Initialize session state for score tracking
if 'score' not in st.session_state:
    st.session_state.score = {'wins': 0, 'losses': 0, 'ties': 0}

# Page layout
st.set_page_config(page_title="Rock Paper Scissors", page_icon="✊")
st.title("🎮 Rock Paper Scissors")
st.markdown("---")

# Game area columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Make your choice:")
    user_option = st.radio(
        "Select your weapon:",
        list(RADIO_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    user_choice = RADIO_OPTIONS[user_option]
    
    if st.button("🚀 Play!", use_container_width=True):
        # Computer makes random choice
        computer_choice = random.choice(['r', 'p', 's'])
        
        # Determine winner
        result = determine_winner(user_choice, computer_choice)
        
        # Update score
        if result == "user":
            st.session_state.score['wins'] += 1
        elif result == "computer":
            st.session_state.score['losses'] += 1
        else:
            st.session_state.score['ties'] += 1
        
        # Store results for display
        st.session_state.last_game = {
            'user_choice': user_choice,
            'computer_choice': computer_choice,
            'result': result
        }

with col2:
    st.subheader("Game Results")
    
    # Display scoreboard
    st.markdown(f"""
    **Scoreboard**  
    🏆 Wins: {st.session_state.score['wins']}  
    😢 Losses: {st.session_state.score['losses']}  
    🤝 Ties: {st.session_state.score['ties']}
    """)
    
    # Display last game result if available
    if 'last_game' in st.session_state:
        st.markdown("---")
        st.subheader("Last Game")
        
        user_emoji = CHOICE_EMOJIS[st.session_state.last_game['user_choice']]
        computer_emoji = CHOICE_EMOJIS[st.session_state.last_game['computer_choice']]
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**You chose:** {user_emoji}")
        with col_b:
            st.markdown(f"**Computer chose:** {computer_emoji}")
        
        if st.session_state.last_game['result'] == "tie":
            st.success("It's a tie! 🎭")
        elif st.session_state.last_game['result'] == "user":
            st.success("You won! 🎉")
        else:
            st.error("You lost! 😢")

# Game instructions
st.markdown("---")
st.markdown("### How to Play")
st.markdown("""
1. Select your choice (Rock, Paper, or Scissors)
2. Click the Play button
3. See who wins!
            
**Rules:**  
- Rock crushes Scissors  
- Scissors cuts Paper  
- Paper covers Rock  
- Same choices result in a tie
""")

# Add some styling
st.markdown("""
<style>
    .stRadio [role=radiogroup] {
        gap: 0.5rem;
    }
    .stRadio [role=radio] {
        padding: 0.75rem;
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    .stRadio [role=radio][aria-checked=true] {
        background-color: #f0f2f6;
        border-color: #4e8cff;
    }
</style>
""", unsafe_allow_html=True)