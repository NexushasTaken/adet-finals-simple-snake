import pygame as py
import random

# === Configurable Grid ===
cols, rows = 30, 20
width, height = 600, 400
tile_width = width / cols
tile_height = height / rows
max_score = cols * rows  # win if snake fills the grid
move_delay = 500  # delay between moves in milliseconds (500ms = 0.5 seconds)

# === Init ===
py.init()
screen = py.display.set_mode((width, height))
clock = py.time.Clock()
font = py.font.SysFont(None, 28)
big_font = py.font.SysFont(None, 64)

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

def draw_text(text, size, x, y, center=False):
    f = big_font if size == 'big' else font
    surface = f.render(text, True, BLACK)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def random_food(snake):
    while True:
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
        food = py.Vector2(x, y)
        if food not in snake:
            return food

def reset_game():
    return [py.Vector2(10, 10), py.Vector2(9, 10), py.Vector2(8, 10)], py.Vector2(1, 0), random_food([])

def draw(snake, food, score, game_over, win):
    screen.fill(WHITE)
    for block in snake:
        py.draw.rect(screen, GREEN, (block.x * tile_width, block.y * tile_height, tile_width, tile_height))
    py.draw.rect(screen, RED, (food.x * tile_width, food.y * tile_height, tile_width, tile_height))

    draw_text(f"Score: {score}", 'small', 10, 10)

    if game_over:
        if win:
            draw_text("YOU WIN!", 'big', width // 2, height // 2 - 30, center=True)
        else:
            draw_text("GAME OVER", 'big', width // 2, height // 2 - 30, center=True)
        draw_text("Press SPACE to restart", 'small', width // 2, height // 2 + 20, center=True)

    py.display.flip()

# === Game Loop ===
snake, direction, food = reset_game()
game_over = False
win = False
last_move_time = py.time.get_ticks()

# Direction buffer - stores the last valid direction change
direction_buffer = py.Vector2(1, 0)  # Initial direction is right (1, 0)

running = True
while running:
    clock.tick(15)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                running = False
            if not game_over:
                # Update the direction buffer if the key press is valid (not opposite of current direction)
                if event.key in (py.K_UP, py.K_w) and direction != py.Vector2(0, 1):
                    direction_buffer = py.Vector2(0, -1)
                elif event.key in (py.K_DOWN, py.K_s) and direction != py.Vector2(0, -1):
                    direction_buffer = py.Vector2(0, 1)
                elif event.key in (py.K_LEFT, py.K_a) and direction != py.Vector2(1, 0):
                    direction_buffer = py.Vector2(-1, 0)
                elif event.key in (py.K_RIGHT, py.K_d) and direction != py.Vector2(-1, 0):
                    direction_buffer = py.Vector2(1, 0)
            if game_over and event.key == py.K_SPACE:
                snake, direction, food = reset_game()
                game_over = False
                win = False

    if not game_over:
        current_time = py.time.get_ticks()
        if current_time - last_move_time >= move_delay:  # Check if enough time has passed
            # Move the snake in the direction stored in the buffer
            direction = direction_buffer

            new_head = snake[0] + direction

            if new_head in snake or not (0 <= new_head.x < cols and 0 <= new_head.y < rows):
                game_over = True
            else:
                snake.insert(0, new_head)

                if new_head == food:
                    food = random_food(snake)
                else:
                    snake.pop()

                if len(snake) == max_score:
                    game_over = True
                    win = True

            last_move_time = current_time  # Update the time of the last move

    draw(snake, food, len(snake) - 3, game_over, win)

py.quit()
