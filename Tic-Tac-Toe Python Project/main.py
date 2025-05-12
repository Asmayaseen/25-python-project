import streamlit as st
import numpy as np

st.set_page_config(page_title="Tic-Tac-Toe 🎮", page_icon="❌⭕")
st.title("Tic-Tac-Toe Game ❌⭕")

# Initialize game state
def initialize_board():
    return np.full((3, 3), '', dtype='U1')

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] != '' and row[0] == row[1] == row[2]:
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] != '' and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] != '' and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != '' and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    # Check for draw
    if '' not in board:
        return 'Draw'
    
    return None

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = initialize_board()
    st.session_state.current_player = '❌'
    st.session_state.winner = None
    st.session_state.moves = 0

# UI Styling
st.markdown("""
    <style>
        .stButton>button {
            height: 80px;
            width: 100%;
            font-size: 36px;
            border-radius: 10px;
            border: 2px solid #f0f2f6;
        }
        .player-turn {
            font-size: 24px;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin: 10px 0;
        }
        .x-turn {
            background-color: #ffebee;
            color: #f44336;
        }
        .o-turn {
            background-color: #e8f5e9;
            color: #4caf50;
        }
    </style>
""", unsafe_allow_html=True)

# Show current player
player_class = "x-turn" if st.session_state.current_player == '❌' else "o-turn"
st.markdown(f"""
    <div class="player-turn {player_class}">
        Current Player: {st.session_state.current_player}
    </div>
""", unsafe_allow_html=True)

# Display the game board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            if st.button(
                st.session_state.board[i][j] or ' ',
                key=f'{i}-{j}',
                disabled=st.session_state.board[i][j] != '' or st.session_state.winner is not None
            ):
                st.session_state.board[i][j] = st.session_state.current_player
                st.session_state.moves += 1
                st.session_state.winner = check_winner(st.session_state.board)
                
                if not st.session_state.winner:
                    st.session_state.current_player = '⭕' if st.session_state.current_player == '❌' else '❌'
                st.rerun()  # Changed from experimental_rerun()

# Game Status
if st.session_state.winner:
    if st.session_state.winner == 'Draw':
        st.success(f"""
            ## It's a Draw! 🤝
            The game ended in a tie after {st.session_state.moves} moves.
        """)
    else:
        st.success(f"""
            ## Player {st.session_state.winner} Wins! 🎉
            Congratulations! Won in {st.session_state.moves} moves.
        """)
    
    if st.button("🔄 Play Again", use_container_width=True):
        st.session_state.board = initialize_board()
        st.session_state.current_player = '❌'
        st.session_state.winner = None
        st.session_state.moves = 0
        st.rerun()  # Changed from experimental_rerun()
else:
    st.info("""
        ### Make your move! 🕹️
        Click on any empty cell to place your symbol.
    """)

# How to Play
with st.expander("ℹ️ How to Play"):
    st.write("""
        **Rules:**
        1. Player ❌ goes first
        2. Take turns marking empty squares
        3. First to get 3 in a row (horizontally, vertically, or diagonally) wins!
        4. If all squares are filled without a winner, it's a draw
    """)