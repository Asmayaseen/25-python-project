import streamlit as st # type: ignore
import numpy as np # type: ignore

st.set_page_config(page_title="Sudoku Solver 🧩", page_icon="🧩")
st.title("Sudoku Solver using Backtracking 🧩✨")

# Sudoku Solver using Backtracking
def is_valid(board, row, col, num):
    # Check Row
    if num in board[row]:
        return False

    # Check Column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 Box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True

# Input Grid UI
def display_grid(board):
    grid = []
    for i in range(9):
        cols = st.columns(9)
        row = []
        for j in range(9):
            val = cols[j].text_input("", str(board[i][j]) if board[i][j] != 0 else "", key=f'{i}-{j}')
            row.append(int(val) if val.isdigit() else 0)
        grid.append(row)
    return grid

def is_valid_grid(grid):
    return all(len(row) == 9 and all(isinstance(x, int) and 0 <= x <= 9 for x in row) for row in grid)

# Initialize
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((9, 9), dtype=int)

st.subheader("Enter your Sudoku Puzzle ⌨️")
st.write("Fill in the numbers and leave empty spaces as blank or 0.")

# Display Grid
st.session_state.board = display_grid(st.session_state.board)

if st.button("Solve Sudoku 🚀"):
    if is_valid_grid(st.session_state.board):
        if solve_sudoku(st.session_state.board):
            st.success("Sudoku Solved Successfully! 🎉")
            st.write(np.array(st.session_state.board))
        else:
            st.error("No solution exists for the given puzzle. 😔")
    else:
        st.warning("Please enter a valid 9x9 Sudoku puzzle! ⚠️")

if st.button("Reset Puzzle 🔄"):
    st.session_state.board = np.zeros((9, 9), dtype=int)
    st.rerun()

st.sidebar.info("Developed with 💖 using Streamlit")
