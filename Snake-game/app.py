import streamlit as st
import numpy as np
import random
import time

# Emojis for visuals
snake_emoji = "🐍"
food_emoji = "🍎"
background_emoji = "⬛"

# Game Variables
width, height = 20, 20
snake_speed = 0.3
score = 0

def initialize_game():
    st.session_state.snake = [[10, 10]]
    st.session_state.direction = "RIGHT"
    st.session_state.food = [random.randint(0, width-1), random.randint(0, height-1)]
    st.session_state.score = 0

if 'snake' not in st.session_state:
    initialize_game()

# UI Design
st.title('🐍 Snake Game using Streamlit')
st.write('Use the buttons to control the snake. Eat the apple to grow!')

# Speed Control
snake_speed = st.slider('Select Speed (Lower is faster)', 0.1, 1.0, 0.3)

# Score Display
st.write(f"**Score:** {st.session_state.score}")

# Restart Button
if st.button('🔄 Restart Game'):
    initialize_game()
    st.rerun()

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('⬆️ Up') and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
with col2:
    if st.button('⬅️ Left') and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
    if st.button('➡️ Right') and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"
with col3:
    if st.button('⬇️ Down') and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"

# Game Board Drawing
def draw_board():
    board = [[background_emoji for _ in range(width)] for _ in range(height)]
    food_x, food_y = st.session_state.food
    board[food_y][food_x] = food_emoji
    for seg in st.session_state.snake:
        board[seg[1]][seg[0]] = snake_emoji
    return '\n'.join([''.join(row) for row in board])

# Snake Movement
def move_snake():
    head = st.session_state.snake[-1][:]

    if st.session_state.direction == "UP":
        head[1] -= 1
    elif st.session_state.direction == "DOWN":
        head[1] += 1
    elif st.session_state.direction == "LEFT":
        head[0] -= 1
    elif st.session_state.direction == "RIGHT":
        head[0] += 1

    # Collision check
    if head in st.session_state.snake or head[0] < 0 or head[1] < 0 or head[0] >= width or head[1] >= height:
        st.error('Game Over! 🥲 Your Score: ' + str(st.session_state.score))
        return False

    st.session_state.snake.append(head)

    # Food Check
    if head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = [random.randint(0, width-1), random.randint(0, height-1)]
    else:
        st.session_state.snake.pop(0)

    return True

# Game Loop
if move_snake():
    st.write(draw_board())
    time.sleep(snake_speed)
    st.rerun()