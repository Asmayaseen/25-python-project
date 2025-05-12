import streamlit as st
import numpy as np
import time

# Initialize board
def initialize_board():
    return np.full((3, 3), '', dtype='U1')

# Optimized winner check
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
    if board[1][1] != '':
        if (board[0][0] == board[1][1] == board[2][2]) or \
           (board[0][2] == board[1][1] == board[2][0]):
            return board[1][1]
    
    return 'Draw' if '' not in board else None

# Minimax with alpha-beta pruning
def minimax(board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    winner = check_winner(board)
    if winner == '⭕': return 1
    if winner == '❌': return -1
    if winner == 'Draw': return 0

    if is_maximizing:
        max_eval = -float('inf')
        for i, j in np.argwhere(board == ''):
            board[i][j] = '⭕'
            eval = minimax(board, depth+1, False, alpha, beta)
            board[i][j] = ''
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in np.argwhere(board == ''):
            board[i][j] = '❌'
            eval = minimax(board, depth+1, True, alpha, beta)
            board[i][j] = ''
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move():
    best_score = -float('inf')
    move = None
    for i, j in np.argwhere(st.session_state.board == ''):
        st.session_state.board[i][j] = '⭕'
        score = minimax(st.session_state.board, 0, False)
        st.session_state.board[i][j] = ''
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

# Initialize game state
if 'board' not in st.session_state:
    st.session_state.board = initialize_board()
    st.session_state.current_player = '❌'
    st.session_state.winner = None
    st.session_state.game_mode = 'ai'  # 'ai' or '2player'

# UI
st.title("❌ Tic-Tac-Toe ⭕")
st.write(f"Current turn: {st.session_state.current_player}")

# Game board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if cols[j].button(
            st.session_state.board[i][j] or ' ',
            key=f'{i}-{j}',
            disabled=st.session_state.board[i][j] != '' or 
                   st.session_state.winner is not None or
                   (st.session_state.game_mode == 'ai' and st.session_state.current_player == '⭕')
        ):
            # Player move
            st.session_state.board[i][j] = st.session_state.current_player
            st.session_state.winner = check_winner(st.session_state.board)
            
            if not st.session_state.winner:
                # Switch turns
                st.session_state.current_player = '⭕' if st.session_state.current_player == '❌' else '❌'
                
                # AI move if in AI mode and it's AI's turn
                if st.session_state.game_mode == 'ai' and st.session_state.current_player == '⭕':
                    with st.spinner('AI thinking...'):
                        time.sleep(0.5)  # Simulate thinking time
                        move = best_move()
                        if move:
                            st.session_state.board[move[0]][move[1]] = '⭕'
                            st.session_state.winner = check_winner(st.session_state.board)
                            st.session_state.current_player = '❌'
            st.rerun()

# Game status
if st.session_state.winner:
    if st.session_state.winner == 'Draw':
        st.success("🤝 It's a draw!")
    else:
        st.balloons()
        st.success(f"🏆 Player {st.session_state.winner} wins!")
    
    if st.button("🔄 Play Again"):
        st.session_state.board = initialize_board()
        st.session_state.current_player = '❌'
        st.session_state.winner = None
        st.rerun()
else:
    if st.session_state.game_mode == 'ai' and st.session_state.current_player == '⭕':
        st.info("AI is thinking...")
    else:
        st.info(f"Player {st.session_state.current_player}'s turn")

# Game mode selector
if st.button("Switch to 2-Player Mode" if st.session_state.game_mode == 'ai' else "Switch to AI Mode"):
    st.session_state.game_mode = '2player' if st.session_state.game_mode == 'ai' else 'ai'
    st.session_state.board = initialize_board()
    st.session_state.current_player = '❌'
    st.session_state.winner = None
    st.rerun()