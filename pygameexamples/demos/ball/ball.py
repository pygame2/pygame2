"""
not much care was taken to make sure demo is correct
just a demonstration of proposed syntax
"""
import pygame2
from pygame2.gl import *


size = width, height = 800, 600
window = pygame2.core.platform.create_window(size=size)
group = pygame2.group.SpriteGroup()

queue = pygame2.core.platform.get_platform_event_queue()
queue.start()

speed = [10, 10]
ball_image = pygame2.core.image.load("ball.gif")
ball_sprite = pygame2.sprite.Sprite(ball_image)
ball_sprite.rect = pygame2.Rect(400, 600, ball_image.width, ball_image.height)

group.add(ball_sprite)


def catch():
    e = glGetError()
    if e:
        print(e)


def upload_texture():
    glBindTexture(GL_TEXTURE_2D, 100)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    image_data = ball_image._data

    width, height = ball_image.width, ball_image.height
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    catch()


def do_vbo():
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    target = 0
    enum = GL_ARRAY_BUFFER
    usage = GL_DYNAMIC_DRAW
    size = len(data)

    glBindBuffer(enum, target)
    catch()
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, 0)
    catch()
    # glBufferData(target, size, data, usage)
    glBufferData(target, 'float', None, usage)
    catch()


upload_texture()
do_vbo()

while 1:
    queue.get()

    rect = ball_sprite.rect
    ball_sprite.rect = rect.move(speed)
    if rect.left < 0 or rect.right >= width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom >= height:
        speed[1] = -speed[1]

    # group.draw()
    window.switch_to()
    catch()

    glClearColor(.5, .5, .5, 1.)
    catch()

    glBindTexture(GL_TEXTURE_2D, 100)
    catch()

    glClear(GL_COLOR_BUFFER_BIT)
    catch()
    window.flip()
