"""
this is a testbed for the opengl operations of pygame2

the general goal is to create new useful functions for pygame2
this testbed is meant to code first, then refactor useful code
into pygame2.
"""
from functools import partial
import os
import pygame2


def on_key_press(*args):
    print('got a key press')


def on_mouse_motion(*args):
    print('got mouse motion')


def main():
    size = 800, 800

    app = pygame2.app.App()
    window = app.create_window(size=size)
    renderer = window.create_renderer()

    def on_draw(*args, **kwargs):
        window.clear()
        renderer.draw()

    window.bind('on_draw', on_draw)
    window.bind('on_key_press', on_key_press)
    window.bind('on_mouse_motion', on_mouse_motion)

    path = os.path.join('resources', 'pygame2-nologo.png')
    texture0 = pygame2.core.image.load(path).create_texture()

    path = os.path.join('resources', 'pygame2.png')
    texture1 = pygame2.core.image.load(path).create_texture()

    animations = list()

    for i in range(4):
        tex = texture0 if i % 2 == 0 else texture1
        renderer.create_sprite(texture=tex)

    def offset(*args):
        for i, sprite in enumerate(renderer.sprites()):
            ani = pygame2.animation.Animation(rotation=i * (360 / 8))
            ani.update_callback = sprite.update_transform
            ani.finish_callback = partial(animations.remove, ani)
            ani.start(sprite)
            animations.append(ani)

    def grow(*args):
        for sprite in renderer.sprites():
            ani = pygame2.animation.Animation(width=3, duration=4)
            ani.update_callback = sprite.update_transform
            ani.finish_callback = partial(animations.remove, ani)
            ani.start(sprite.rect)
            animations.append(ani)

    def shrink(*args):
        for sprite in renderer.sprites():
            ani = pygame2.animation.Animation(width=1, duration=1)
            ani.update_callback = sprite.update_transform
            ani.finish_callback = partial(animations.remove, ani)
            ani.start(sprite.rect)
            animations.append(ani)

    def reset_rotation(*args):
        def reset(ani, sprite):
            sprite.rotation = 0
            animations.remove(ani)

        for sprite in renderer.sprites():
            r = sprite.rotation
            dr = 360 - r
            ani = pygame2.animation.Animation(rotation=r + 360 + dr)
            ani.update_callback = sprite.update_transform
            ani.finish_callback = partial(reset, ani, sprite)
            ani.start(sprite)
            animations.append(ani)

    def boo_ya_ka_sha(*args):
        offset()
        app.clock.schedule(grow, 1.5)
        app.clock.schedule(shrink, 5.5)
        app.clock.schedule(reset_rotation, 5.5)

    def update(dt):
        for ani in animations:
            ani.update(dt)

    boo_ya_ka_sha()
    app.clock.schedule(boo_ya_ka_sha, 7, repeat=True)
    app.clock.schedule(update, 1 / 70., repeat=True)

    # this will start the application and will exit when window is closed
    app.run()


if __name__ == '__main__':
    main()
