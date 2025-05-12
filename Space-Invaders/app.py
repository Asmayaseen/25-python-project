import streamlit as st
import numpy as np
import random
import time

# Initialize game variables
if 'spaceship_pos' not in st.session_state:
    st.session_state.spaceship_pos = 5
    st.session_state.enemy_pos = [random.randint(0, 9) for _ in range(5)]
    st.session_state.bullet_pos = -1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.last_update = time.time()

# Display game
st.title("🚀 Space Invaders with Streamlit")

def render_game():
    grid = np.full((10, 10), ' ')
    
    # Place enemies
    for pos in st.session_state.enemy_pos:
        grid[0, pos] = '👾'
    
    # Place bullet if active
    if st.session_state.bullet_pos != -1:
        if st.session_state.bullet_pos >= 0:
            grid[st.session_state.bullet_pos, st.session_state.spaceship_pos] = '💥'
            st.session_state.bullet_pos -= 1
            
            # Check for enemy hit
            if st.session_state.bullet_pos == 0 and st.session_state.spaceship_pos in st.session_state.enemy_pos:
                st.session_state.enemy_pos.remove(st.session_state.spaceship_pos)
                st.session_state.score += 1
                st.session_state.bullet_pos = -1
                # Add new enemy
                st.session_state.enemy_pos.append(random.randint(0, 9))
        else:
            st.session_state.bullet_pos = -1

    # Place spaceship
    grid[9, st.session_state.spaceship_pos] = '🚀'
    
    # Game over condition
    if any(pos == 9 for pos in st.session_state.enemy_pos):
        st.session_state.game_over = True

    # Display the grid
    st.text("\n".join([" ".join(row) for row in grid]))
    st.write(f"Score: {st.session_state.score}")

# Game controls
if st.session_state.game_over:
    st.error("Game Over! Refresh to restart.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Left"):
            st.session_state.spaceship_pos = max(0, st.session_state.spaceship_pos - 1)
    with col2:
        if st.button("🚀 Fire") and st.session_state.bullet_pos == -1:
            st.session_state.bullet_pos = 8
    with col3:
        if st.button("➡️ Right"):
            st.session_state.spaceship_pos = min(9, st.session_state.spaceship_pos + 1)

# Game loop implementation
current_time = time.time()
if current_time - st.session_state.last_update > 0.5:  # Update every 0.5 seconds
    render_game()
    st.session_state.last_update = current_time
    st.rerun()  # Use st.rerun() instead of experimental_rerun()
else:
    render_game()