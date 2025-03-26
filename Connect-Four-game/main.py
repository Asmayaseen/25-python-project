import numpy as np
import streamlit as st
import random
import time

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1  # 💙 Blue
AI_PIECE = 2  # 💛 Yellow

# Function to create the board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

# Function to drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if a column is valid for a move
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Get the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None

# Check for a winning move
def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r, c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i, c] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i, c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i, c + i] == piece for i in range(4)):
                return True

    return False

# Convert board numbers to emoji format
def board_to_emoji(board):
    emoji_map = {0: "⚪", 1: "💙", 2: "💛"}
    return [[emoji_map[cell] for cell in row] for row in np.flip(board, 0)]

# Streamlit UI Setup
st.title("🎯 Connect Four – Customized Version")

# Session state initialization
if "board" not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.turn = random.randint(PLAYER, AI)

# Display board
st.write("### Click on a column to drop a piece:")
columns = st.columns(COLUMN_COUNT)

# Turn Indicator
if not st.session_state.game_over:
    if st.session_state.turn == PLAYER:
        st.markdown("### **💙 Player's Turn**")
    else:
        st.markdown("### **💛 AI's Turn**")

# Player move - Clickable columns
if not st.session_state.game_over and st.session_state.turn == PLAYER:
    for i, col in enumerate(columns):
        if col.button(f"{i}"):
            if is_valid_location(st.session_state.board, i):
                row = get_next_open_row(st.session_state.board, i)
                drop_piece(st.session_state.board, row, i, PLAYER_PIECE)

                if winning_move(st.session_state.board, PLAYER_PIECE):
                    st.session_state.winner = "🎉 Congratulations! You Won! 💙"
                    st.session_state.game_over = True
                else:
                    st.session_state.turn = AI  # Switch to AI
                    time.sleep(1)
            else:
                st.warning("Column is full. Try another one!")
            st.rerun()

# AI move
if not st.session_state.game_over and st.session_state.turn == AI:
    st.write("🤖 AI is thinking...")
    time.sleep(1)
    valid_moves = [c for c in range(COLUMN_COUNT) if is_valid_location(st.session_state.board, c)]
    if valid_moves:
        ai_col = random.choice(valid_moves)
        row = get_next_open_row(st.session_state.board, ai_col)
        drop_piece(st.session_state.board, row, ai_col, AI_PIECE)

        if winning_move(st.session_state.board, AI_PIECE):
            st.session_state.winner = "🤖 AI Wins! 💛"
            st.session_state.game_over = True
        else:
            st.session_state.turn = PLAYER  # Switch back to player
    st.rerun()

# Display updated board
st.table(board_to_emoji(st.session_state.board))

# Display winner message
if st.session_state.game_over and "winner" in st.session_state:
    st.markdown(f"## {st.session_state.winner}")

# Restart game button
if st.session_state.game_over:
    if st.button("Restart Game"):
        st.session_state.board = create_board()
        st.session_state.game_over = False
        st.session_state.turn = random.randint(PLAYER, AI)
        st.rerun()

# Footer
st.markdown("---")
st.markdown("### Customized by **Asma Yaseen** 👩‍💻")