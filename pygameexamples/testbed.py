"""
this is a testbed for the opengl operations of pygame2

the general goal is to create new useful functions for pygame2
this testbed is meant to code first, then refactor useful code
into pygame2.
"""
import os
import pygame2
from pygame2.graphics import *


def on_key_press(*args):
    print('got a key press')


def on_mouse_motion(*args):
    print('got mouse motion')


def main():
    size = 800, 800

    window = pygame2.core.platform.create_window(size=size)
    app = pygame2.app.App()
    program_id = create_program()

    path = os.path.join('resources', 'pygame2-nologo.png')
    texture0 = pygame2.core.image.load(path).create_texture()

    path = os.path.join('resources', 'pygame2.png')
    texture1 = pygame2.core.image.load(path).create_texture()

    renderer = pygame2.renderer.SpriteRenderer(program_id)

    for i in range(4):
        if i % 2 == 0:
            sprite = pygame2.sprite.Sprite(texture=texture0)
        else:
            sprite = pygame2.sprite.Sprite(texture=texture1)

        sprite.rotation = i * (360 / 4)
        renderer.add(sprite)

    def on_draw(*args, **kwargs):
        window.clear()
        renderer.draw()

    window.bind('on_draw', on_draw)
    window.bind('on_key_press', on_key_press)
    window.bind('on_mouse_motion', on_mouse_motion)

    def update(dt):
        for i, sprite in enumerate(renderer.sprites()):
            sprite.rect.width += .1 * dt
            sprite.rect.height += .05 * dt
            sprite.rotation += 20 * i * dt
            sprite.update_transform()

    app.clock.schedule(update, 1 / 70., repeat=True)

    # this will start the application and will exit when window is closed
    app.run(window)


if __name__ == '__main__':
    main()
