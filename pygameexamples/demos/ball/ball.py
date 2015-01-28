"""
import sys
import pygame2 as pygame
from pygame2.compat import *

pygame.init()
size = width, height = 800, 600
speed = [10, 10]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right >= width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom >= height:
        speed[1] = -speed[1]
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
"""

# rewritten in pygame-too style
# not much care was taken to make sure demo is correct
# just a demonstration of proposed syntax

import pygame2

size = width, height = 800, 600
window = pygame2.get_display().create_window(size=size)
group = pygame2.group.SpriteGroup()

speed = [10, 10]
ball_image = pygame2.core.image.load("ball.gif")
ball_sprite = pygame2.sprite.Sprite(ball_image)

group.add(ball_sprite)

while 1:
    pygame2.event.pump()

    rect = ball_sprite.rect
    ball_sprite.rect = rect.move(speed)
    if rect.left < 0 or rect.right >= width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom >= height:
        speed[1] = -speed[1]

    group.draw()
