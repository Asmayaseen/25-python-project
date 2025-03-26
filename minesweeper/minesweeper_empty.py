import random
import streamlit as st # type: ignore

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set()

    def make_new_board(self):
        board = [[0 for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if self.board[r][c] == '*':
                    num_bombs += 1
        return num_bombs

    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if (r, c) not in self.dug:
                    self.dig(r, c)
        return True

    def get_display_board(self):
        display_board = [[' ' if (r, c) not in self.dug else str(self.board[r][c]) if self.board[r][c] != 0 else '0' for c in range(self.dim_size)] for r in range(self.dim_size)]
        return display_board

def play(dim_size=10, num_bombs=10):
    st.title('Minesweeper')
    board = Board(dim_size, num_bombs)
    
    if 'board' not in st.session_state:
        st.session_state.board = board
        st.session_state.game_over = False

    def update_board(row, col):
        if st.session_state.game_over:
            return
        if not board.dig(row, col):
            st.session_state.game_over = True
            st.error('Game Over! You hit a bomb!')
        elif len(board.dug) == dim_size**2 - num_bombs:
            st.success('Congratulations! You Win!')
            st.session_state.game_over = True

    for row in range(dim_size):
        cols = st.columns(dim_size)
        for col in range(dim_size):
            label = st.session_state.board.get_display_board()[row][col]
            if label == ' ' and not st.session_state.game_over:
                if cols[col].button(' ', key=f'{row}-{col}'):
                    update_board(row, col)
            else:
                cols[col].button(label, disabled=True, key=f'{row}-{col}-disabled')

if __name__ == '__main__':
    play()
