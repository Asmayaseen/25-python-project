import streamlit as st
import random
import time

# Emojis for visuals
snake_emoji = "🐍"
food_emoji = "🍎"
background_emoji = "⬛"

# Game Variables
width, height = 20, 20
snake_speed = 0.3

def initialize_game():
    st.session_state.snake = [[10, 10]]
    st.session_state.direction = "RIGHT"
    st.session_state.food = [random.randint(0, width-1), random.randint(0, height-1)]
    st.session_state.score = 0
    st.session_state.game_active = True

if 'snake' not in st.session_state:
    initialize_game()

# UI Design
st.title('🐍 Snake Game using Streamlit')
st.write('Use the buttons to control the snake. Eat the apple to grow!')

# Speed Control
snake_speed = st.slider('Select Speed (Lower is faster)', 0.1, 1.0, 0.3)

# Score Display
st.write(f"**Score:** {st.session_state.score}")

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

# Restart Button
if st.button('🔄 Restart Game'):
    initialize_game()
    st.rerun()

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
    if not st.session_state.game_active:
        return False
        
    head = st.session_state.snake[-1][:]

    if st.session_state.direction == "UP":
        head[1] -= 1
    elif st.session_state.direction == "DOWN":
        head[1] += 1
    elif st.session_state.direction == "LEFT":
        head[0] -= 1
    elif st.session_state.direction == "RIGHT":
        head[0] += 1

    # Wall collision check
    if head[0] < 0 or head[1] < 0 or head[0] >= width or head[1] >= height:
        st.session_state.game_active = False
        return False

    # Self collision check
    if head in st.session_state.snake:
        st.session_state.game_active = False
        return False

    st.session_state.snake.append(head)

    # Food Check
    if head == st.session_state.food:
        st.session_state.score += 1
        while True:
            new_food = [random.randint(0, width-1), random.randint(0, height-1)]
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.pop(0)

    return True

# Main Game Display
if st.session_state.game_active:
    if move_snake():
        st.write(draw_board())
        time.sleep(snake_speed)
        st.rerun()
else:
    st.error(f'Game Over! 🥲 Your Score: {st.session_state.score}')
    st.write(draw_board())
    if st.button('🎮 Play Again'):
        initialize_game()
        st.rerun()