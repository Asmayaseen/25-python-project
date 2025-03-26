import streamlit as st
import random

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
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
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

# Streamlit UI
def main():
    st.title('💣 Minesweeper in Streamlit 🎮')
    st.write('Click a tile to reveal it. Avoid bombs! 💥')

    dim_size = st.slider('Choose Board Size:', 5, 15, 10)
    num_bombs = st.slider('Choose Number of Bombs:', 1, min(dim_size*dim_size//4, 25), 10)

    if 'board' not in st.session_state or st.session_state.reset:
        st.session_state.board = Board(dim_size, num_bombs)
        st.session_state.game_over = False
        st.session_state.reset = False

    board = st.session_state.board

    if st.session_state.game_over:
        st.error('💥 Game Over! You hit a bomb.')
    elif len(board.dug) == dim_size**2 - num_bombs:
        st.success('🎉 Congratulations! You Win!')
        st.balloons()
        st.session_state.game_over = True

    cols = st.columns(dim_size)
    for r in range(dim_size):
        for c in range(dim_size):
            if (r, c) in board.dug:
                cell_value = board.board[r][c]
                display_value = '💣' if cell_value == '*' else str(cell_value) if cell_value > 0 else ' '
                cols[c].write(f'**{display_value}**')
            else:
                if cols[c].button(' ', key=f'{r},{c}') and not st.session_state.game_over:
                    if not board.dig(r, c):
                        st.session_state.game_over = True

    if st.session_state.game_over or len(board.dug) == dim_size**2 - num_bombs:
        if st.button('🔄 Restart Game'):
            st.session_state.reset = True
            st.rerun()

if __name__ == '__main__':
    main()
