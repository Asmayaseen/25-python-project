import streamlit as st
import numpy as np

st.set_page_config(page_title="Sudoku Solver 🧩", layout="centered")
st.title("Sudoku Solver 🧩")
st.write("Enter your Sudoku puzzle and let the solver do its magic! ✨")

def is_valid(board, num, pos):
    # Check row
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
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

    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
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

st.write("Use 0 for empty cells")

# Input Grid
board = []
st.write("### Enter your Sudoku Puzzle:")

cols = [st.columns(9) for _ in range(9)]

for i in range(9):
    row = []
    for j in range(9):
        cell = cols[i][j].number_input(f"{i+1},{j+1}", min_value=0, max_value=9, value=0, step=1)
        row.append(cell)
    board.append(row)

if st.button("Solve Puzzle 🧩"):
    if solve(board):
        st.success("Puzzle Solved! 🎉")
        st.code(display_board(board))
    else:
        st.error("No solution exists! 🚫")

st.write("Good luck solving more puzzles! 💡")
