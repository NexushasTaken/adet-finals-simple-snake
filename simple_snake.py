import pygame as py
import random

py.init()
screen = py.display.set_mode((600, 400))
clock = py.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

snake = [py.Vector2(100, 100)]
direction = py.Vector2(1, 0)  # normalized
speed = 10
food = py.Vector2(300, 200)

def draw():
    screen.fill(WHITE)
    for block in snake:
        py.draw.rect(screen, GREEN, (*block, 10, 10))
    py.draw.rect(screen, RED, (*food, 10, 10))
    py.display.flip()

def random_food():
    x = random.randrange(0, 600, 10)
    y = random.randrange(0, 400, 10)
    return py.Vector2(x, y)

running = True
while running:
    clock.tick(15)

    for event in py.event.get():
        if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP and direction != py.Vector2(0, 1):
                direction = py.Vector2(0, -1)
            elif event.key == py.K_DOWN and direction != py.Vector2(0, -1):
                direction = py.Vector2(0, 1)
            elif event.key == py.K_LEFT and direction != py.Vector2(1, 0):
                direction = py.Vector2(-1, 0)
            elif event.key == py.K_RIGHT and direction != py.Vector2(-1, 0):
                direction = py.Vector2(1, 0)

    new_head = snake[0] + direction * speed

    if new_head in snake or not (0 <= new_head.x < 600 and 0 <= new_head.y < 400):
        running = False
        break

    snake.insert(0, new_head)

    if new_head == food:
        food = random_food()
    else:
        snake.pop()

    draw()

py.quit()
