import streamlit as st # type: ignore
import numpy as np # type: ignore

st.set_page_config(page_title="Tic-Tac-Toe 🎮", page_icon="❌⭕")
st.title("Tic-Tac-Toe Game ❌⭕")

# Initialize game state
def initialize_board():
    return np.full((3, 3), '')

def check_winner(board):
    for row in board:
        if all(cell == row[0] and cell != '' for cell in row):
            return row[0]
    for col in range(3):
        if all(board[row][col] == board[0][col] and board[row][col] != '' for row in range(3)):
            return board[0][col]
    if all(board[i][i] == board[0][0] and board[i][i] != '' for i in range(3)) or \
       all(board[i][2-i] == board[0][2] and board[i][2-i] != '' for i in range(3)):
        return board[1][1]
    if '' not in board:
        return 'Draw'
    return None

if 'board' not in st.session_state:
    st.session_state.board = initialize_board()
    st.session_state.current_player = '❌'
    st.session_state.winner = None

st.write(f"Current Player: {st.session_state.current_player}")

# Display Board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if cols[j].button(st.session_state.board[i][j] or ' ', key=f'{i}-{j}') and not st.session_state.winner:
            if st.session_state.board[i][j] == '':
                st.session_state.board[i][j] = st.session_state.current_player
                winner = check_winner(st.session_state.board)
                if winner:
                    st.session_state.winner = winner
                else:
                    st.session_state.current_player = '⭕' if st.session_state.current_player == '❌' else '❌'

# Game Status
if st.session_state.winner:
    if st.session_state.winner == 'Draw':
        st.success("It's a Draw! 🤝")
    else:
        st.success(f"Player {st.session_state.winner} Wins! 🥳")
    if st.button("Restart Game 🔄"):
        st.session_state.board = initialize_board()
        st.session_state.current_player = '❌'
        st.session_state.winner = None
else:
    st.info("Make your move! 🕹️")
