"""
this is a testbed for the opengl operations of pygame2

the general goal is to create new useful functions for pygame2
this testbed is meant to code first, then refactor useful code
into pygame2.  mostly, things will be moved into pygame2.graphics.
"""
import os
import pygame2
from pygame2.graphics import *


def main():
    size = 800, 800

    window = pygame2.core.platform.create_window(size=size)
    app = pygame2.app.App()
    program_id = create_program()
    path = os.path.join('resources', 'pygame2-nologo.png')
    texture = pygame2.core.image.load(path).create_texture()
    group = pygame2.group.SpriteGroup(program_id, texture)

    for i in range(4):
        sprite = pygame2.sprite.Sprite()
        sprite.rotation = i * (360 / 4)
        group.add(sprite)

    def on_draw(*args, **kwargs):
        window.clear()
        group.draw()

    window.bind('on_draw', on_draw)

    def update(dt):
        for i, sprite in enumerate(group.sprites()):
            sprite.rotation += 20 * i * dt
            sprite.update_transform()

    app.clock.schedule(update, 1 / 70., repeat=True)

    # this will start the application and will exit when window is closed
    app.run(window)


if __name__ == '__main__':
    main()
