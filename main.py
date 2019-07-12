# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
import random

pygame.init()

screen_width = 500
screen_height = 500
min_px = 20

# speed config
snake_speed = 15
current_speed = snake_speed
max_speed = 20

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("贪吃蛇")

clock = pygame.time.Clock()

# images
background = pygame.transform.scale(pygame.image.load('resource/img/background.jpg'), (screen_width, screen_height))
snake_shape = pygame.transform.scale(pygame.image.load('resource/img/snake.jpg'), (min_px, min_px))
food = pygame.transform.scale(pygame.image.load('resource/img/food.jpg'), (min_px, min_px))


# game over
def game_over():
    print('quit')
    pygame.quit()
    sys.exit()


# generate position
def generate_position(exist_position):
    x_list = list(range(0, screen_width, min_px))
    y_list = list(range(0, screen_height, min_px))

    for x, y in exist_position:
        if x in x_list:
            x_list.remove(x)
        if y in y_list:
            y_list.remove(y)

    record = (random.choice(x_list), random.choice(y_list))
    return record


# default position and length
snake_length = 1
position_x, position_y = generate_position([(0, 0)])
position_list = [(position_x, position_y)]

# default food position
food_position = generate_position(position_list)

# default direction
snake_direction = []

while True:
    # set background
    screen.blit(background, (0, 0))

    # listen keyboard event
    for event in pygame.event.get():
        # quit when click quit
        if event.type == pygame.QUIT:
            game_over()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and (not snake_direction or snake_direction[-1] not in ['up', 'down']):
                snake_direction.append('down')
            elif event.key == pygame.K_UP and (not snake_direction or snake_direction[-1] not in ['up', 'down']):
                snake_direction.append('up')
            elif event.key == pygame.K_LEFT and (not snake_direction or snake_direction[-1] not in ['right', 'left']):
                snake_direction.append('left')
            elif event.key == pygame.K_RIGHT and (not snake_direction or snake_direction[-1] not in ['right', 'left']):
                snake_direction.append('right')
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT, {}))

    # control snake speed
    if current_speed < max_speed:
        current_speed += 1
    else:
        # modify position depend snake's direction
        if snake_direction:
            if len(snake_direction) > 1:
                direction = snake_direction.pop(0)
            else:
                direction = snake_direction[0]
            if direction == 'down':
                position_y += min_px
            elif direction == 'up':
                position_y -= min_px
            elif direction == 'left':
                position_x -= min_px
            elif direction == 'right':
                position_x += min_px
            current_speed = snake_speed

        # add new position
        position_list.append((position_x, position_y))

        # if snake length more than position length, position pop index 0
        if len(position_list) > snake_length:
            position_list.pop(0)

        # if eat food position list, snake length add 1, regenerate food position
        if food_position == position_list[-1]:
            snake_length += 1
            food_position = generate_position(position_list)

    # render all position
    for position in position_list:
        screen.blit(snake_shape, position)

    # set food position
    screen.blit(food, food_position)

    # constraint snake can't crash self
    if any(p == position_list[-1] for p in position_list[:-1]):
        game_over()

    # constraint snake can't out screen
    if not (0 <= position_x < screen_width):
        game_over()
    if not (0 <= position_y < screen_height):
        game_over()

    # update screen
    pygame.display.update()
    clock.tick(60)
