"""
this is a testbed for the opengl operations of pygame2

the general goal is to create new useful functions for pygame2
this testbed is meant to code first, then refactor useful code
into pygame2.  mostly, things will be moved into pygame2.graphics.
"""
import pygame2
from pygame2.graphics import *


def main():
    size = 800, 800

    window = pygame2.core.platform.create_window(size=size)
    app = pygame2.app.App()
    program_id = create_program()
    texture = load_texture()

    group = pygame2.group.SpriteGroup(program_id, texture)
    sprite = pygame2.sprite.Sprite()

    group.add(sprite)

    def on_draw(*args, **kwargs):
        window.clear()
        group.draw()

    window.bind('on_draw', on_draw)

    def update(dt):
        sprite.rotation += 10 * dt
        sprite.update_vbo()

    app.clock.schedule(update, 1 / 50., repeat=True)

    app.run(window)


if __name__ == '__main__':
    main()
