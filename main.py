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
snake_speed = 1
current_speed = snake_speed
max_speed = 10

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("贪吃蛇")

clock = pygame.time.Clock()

# images
background = pygame.transform.scale(pygame.image.load('resource/img/background.jpg'), (screen_width, screen_height))
snake_shape = pygame.transform.scale(pygame.image.load('resource/img/snake.jpg'), (min_px, min_px))
food = pygame.transform.scale(pygame.image.load('resource/img/food.jpg'), (min_px, min_px))

# font
font = pygame.font.Font('resource/font/myfont.ttf', 80)
death_message1 = font.render("你已经死了", True, (0, 0, 0), (255, 255, 255))
death_message2 = font.render("点击我或者", True, (0, 0, 0), (255, 255, 255))
death_message3 = font.render("回车键重新", True, (0, 0, 0), (255, 255, 255))
death_message4 = font.render("　　　开始", True, (0, 0, 0), (255, 255, 255))
death_message_list = [death_message1, death_message2, death_message3, death_message4]

death = False
death_region = Rect(0, 0, 0, 0)


def show_death_message():
    death_rect = death_message1.get_rect()
    x, y, w, h = death_rect
    new_h = h
    for i in range(0, len(death_message_list)):
        screen.blit(death_message_list[i], (50, 100+h*i))
        new_h += h
    new_rect = Rect(50+x, 100+y, w, new_h-h)
    return new_rect


def position_in_rect(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
        return True
    return False


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

# scrap position to store to before position
scrap_position = []

while True:
    # set background
    screen.blit(background, (0, 0))

    # listen keyboard event
    for event in pygame.event.get():
        # quit when click quit
        if event.type == pygame.QUIT:
            game_over()

        elif event.type == pygame.KEYDOWN:
            if not death:
                if event.key == pygame.K_DOWN and (not snake_direction or snake_direction[-1] not in ['up', 'down']):
                    snake_direction.append('down')
                elif event.key == pygame.K_UP and (not snake_direction or snake_direction[-1] not in ['up', 'down']):
                    snake_direction.append('up')
                elif event.key == pygame.K_LEFT and (not snake_direction or snake_direction[-1] not in ['right', 'left']):
                    snake_direction.append('left')
                elif event.key == pygame.K_RIGHT and (not snake_direction or snake_direction[-1] not in ['right', 'left']):
                    snake_direction.append('right')

            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT, {}))
            elif event.key == pygame.K_RETURN:
                death = False
                death_region = Rect(0, 0, 0, 0)
                snake_length = 1
                position_x, position_y = generate_position([(0, 0)])
                position_list = [(position_x, position_y)]
                food_position = generate_position(position_list)
                snake_direction = []
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if position_in_rect(event.pos, death_region):
                death = False
                death_region = Rect(0, 0, 0, 0)
                snake_length = 1
                position_x, position_y = generate_position([(0, 0)])
                position_list = [(position_x, position_y)]
                food_position = generate_position(position_list)
                snake_direction = []

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
        if len(position_list) > snake_length and not death:
            pre_pos = position_list.pop(0)
            scrap_position.append(pre_pos)
            if len(scrap_position) > 2:
                scrap_position.pop(0)

        # show right length when death
        if death:
            position_list.insert(0, scrap_position[1])
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
        death_region = show_death_message()
        death = True

    # constraint snake can't out screen
    if not (0 <= position_x < screen_width):
        death_region = show_death_message()
        death = True
    if not (0 <= position_y < screen_height):
        death_region = show_death_message()
        death = True

    # update screen
    pygame.display.update()
    clock.tick(60)
