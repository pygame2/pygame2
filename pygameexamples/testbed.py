"""
this is a testbed for the opengl operations of pygame2

the general goal is to create new useful functions for pygame2
this testbed is meant to code first, then refactor useful code
into pygame2.
"""
from functools import partial
import os
import pygame2


def load_texture(filename):
    path = os.path.join('resources', filename)
    return pygame2.core.image.load(path).create_texture()


def offset(sprites):
    for i, sprite in enumerate(sprites):
        yield sprite.animate(rotation=i * (360 / 8), transition='in_out_quad')


def grow(sprites):
    for sprite in sprites:
        yield sprite.rect.animate(width=3, height=1.5, duration=3,
                                  transition='in_out_quint')


def shrink(sprites):
    for sprite in sprites:
        yield sprite.rect.animate(width=1, height=1, duration=1.35)


def reset_rotation(sprites):
    for sprite in sprites:
        ani = sprite.animate(rotation=720, duration=1.5)
        ani.bind('on_finish', partial(setattr, sprite, 'rotation', 0))
        yield ani


def main():
    window_size = 800, 800
    animations = list()

    app = pygame2.app.App()
    window = app.create_window(size=window_size)

    def on_draw(*args, **kwargs):
        for sprite in renderer.sprites():
            sprite.update_transform()
        window.clear()
        renderer.draw()

    window.bind('on_draw', on_draw)

    texture0 = load_texture('pygame2-nologo.png')
    texture1 = load_texture('pygame2.png')

    renderer = window.create_renderer()
    for i in range(8):
        texture = texture0 if i % 2 == 0 else texture1
        renderer.create_sprite(texture=texture)

    def play_animation(func, dt):
        for ani in func(renderer.sprites()):
            ani.bind('on_finish', partial(animations.remove, ani))
            animations.append(ani)

    def update(dt):
        for ani in animations:
            ani.update(dt)

    def boo_ya_ka_sha(*args):
        sched = app.clock.schedule
        sched(partial(play_animation, offset), 0)
        sched(partial(play_animation, grow), 1)
        sched(partial(play_animation, shrink), 5)
        sched(partial(play_animation, reset_rotation), 5)

    boo_ya_ka_sha()
    app.clock.schedule(boo_ya_ka_sha, 8, repeat=True)
    app.clock.schedule(update, 1 / 40., repeat=True)

    # this will start the application and will exit when window is closed
    app.run()


if __name__ == '__main__':
    main()
