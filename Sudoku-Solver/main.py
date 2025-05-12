import streamlit as st
import numpy as np

# Page Config
st.set_page_config(page_title="Sudoku Solver 🧩", layout="centered")
st.title("Sudoku Solver 🧩")
st.markdown("Enter your Sudoku puzzle and let the solver do its magic! ✨")

# Sudoku Solver Functions
def is_valid(board, num, pos):
    # Check row
    if num in board[pos[0]] and board[pos[0]].index(num) != pos[1]:
        return False

    # Check column
    if num in [board[i][pos[1]] for i in range(9) if i != pos[0]]:
        return False

    # Check 3x3 box
    box_x, box_y = pos[1] // 3, pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False

def display_board(board):
    board_str = ""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            board_str += "-" * 21 + "\n"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                board_str += "| "
            board_str += str(board[i][j]) if board[i][j] != 0 else "."
            board_str += " "
        board_str += "\n"
    return board_str

# UI Improvements
st.markdown("### Enter your Sudoku Puzzle (Use **0** for empty cells)")

# Create a 9x9 grid using st.columns
cols = st.columns(9)
board = [[0 for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        with cols[j]:
            board[i][j] = st.number_input(
                f"Row {i+1}, Col {j+1}",
                min_value=0,
                max_value=9,
                value=0,
                key=f"cell_{i}_{j}",
                step=1
            )

# Solve Button
if st.button("Solve Puzzle 🧩", type="primary"):
    if solve(board):
        st.success("✅ Puzzle Solved! 🎉")
        st.code(display_board(board))
    else:
        st.error("❌ No solution exists! 🚫")

st.markdown("---")
st.markdown("### How to Use?")
st.markdown("1. Enter numbers (1-9) in the grid.")
st.markdown("2. Use **0** for empty cells.")
st.markdown("3. Click **Solve Puzzle** button.")
st.markdown("4. Enjoy the solution! 😊")