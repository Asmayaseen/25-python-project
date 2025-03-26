import streamlit as st # type: ignore
import numpy as np # type: ignore
import random
import time

# Initialize game variables
st.session_state.setdefault('spaceship_pos', 5)
st.session_state.setdefault('enemy_pos', [random.randint(0, 9) for _ in range(5)])
st.session_state.setdefault('bullet_pos', -1)
st.session_state.setdefault('score', 0)
st.session_state.setdefault('game_over', False)

# Display game
st.title("🚀 Space Invaders with Streamlit")

def render_game():
    grid = np.full((10, 10), ' ')
    
    # Place enemies
    for pos in st.session_state.enemy_pos:
        grid[0, pos] = '👾'
    
    # Place bullet
    if st.session_state.bullet_pos != -1:
        grid[st.session_state.bullet_pos, st.session_state.spaceship_pos] = '💥'
        st.session_state.bullet_pos -= 1

    # Check for collisions
    if 0 <= st.session_state.bullet_pos < 10 and grid[st.session_state.bullet_pos, st.session_state.spaceship_pos] == '👾':
        st.session_state.enemy_pos.remove(st.session_state.spaceship_pos)
        st.session_state.score += 1
        st.session_state.bullet_pos = -1

    # Place spaceship
    grid[9, st.session_state.spaceship_pos] = '🚀'
    
    # Game over condition
    if any(pos == 9 for pos in st.session_state.enemy_pos):
        st.session_state.game_over = True

    # Display the grid
    st.write("\n".join([" ".join(row) for row in grid]))
    st.write(f"Score: {st.session_state.score}")

# Controls
if st.session_state.game_over:
    st.error("Game Over! Refresh to restart.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Left"):
            st.session_state.spaceship_pos = max(0, st.session_state.spaceship_pos - 1)
    with col2:
        if st.button("🚀 Fire"):
            if st.session_state.bullet_pos == -1:
                st.session_state.bullet_pos = 8
    with col3:
        if st.button("➡️ Right"):
            st.session_state.spaceship_pos = min(9, st.session_state.spaceship_pos + 1)

# Update game state and render
render_game()
