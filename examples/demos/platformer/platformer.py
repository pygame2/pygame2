"""
this is a testbed for the opengl operations of pygame2

the general goal is to create new useful functions for pygame2
this testbed is meant to code first, then refactor useful code
into pygame2.
"""
from functools import partial
import os
import pygame2


def load_texture(renderer, *args):
    path = os.path.join('..', '..', 'resources', *args)
    return renderer.create_texture(pygame2.core.image.load(path))


def main():
    window_size = 800, 800
    desired_fps = 1 / 60.
    animations = list()

    app = pygame2.app.App()
    window = app.create_window(size=window_size)

    axis_animations = dict()

    def on_key_press(*args, **kwargs):
        print(args, kwargs)
        key, junk = kwargs['args']
        # possibly only for windows

        # up
        ani = None
        axis = None
        duration = .6
        if key == 65362:
            ani = player_sprite.rect.animate(y=player_sprite.rect.y + .1,
                                             duration=duration)
            axis = 'y'
        # right
        elif key == 65363:
            ani = player_sprite.rect.animate(x=player_sprite.rect.x + .1,
                                             duration=duration)
            axis = 'x'
        # down
        elif key == 65364:
            ani = player_sprite.rect.animate(y=player_sprite.rect.y - .1,
                                             duration=duration)
            axis = 'y'
        # left
        elif key == 65361:
            ani = player_sprite.rect.animate(x=player_sprite.rect.x - .1,
                                             duration=duration)
            axis = 'x'

        # space
        elif key == 32:
            ani = player_sprite.animate(rotation=360, duration=.75,
                                        transition='out_quint')
            ani.subscribe('on_finish', partial(setattr, player_sprite, 'rotation', 0))
            axis = 'z'

        if ani:
            old = axis_animations.get(axis, None)
            if old is not None:
                try:
                    old.abort()
                except RuntimeError:  # if already aborted
                    pass
            axis_animations[axis] = ani
            ani.subscribe('on_finish', partial(animations.remove, ani))
            animations.append(ani)

    def update(dt):
        for ani in animations:
            ani.update(dt)

    def on_draw(*args, **kwargs):
        for sprite in renderer.sprites():
            sprite.update_transform()
        window.clear()
        renderer.draw()

    window.subscribe('on_draw', on_draw)
    window.subscribe('on_key_press', on_key_press)

    renderer = window.create_renderer()
    loader = partial(load_texture, renderer)

    texture = loader('backgrounds', 'colored_grass.png')
    background_sprite = renderer.create_sprite(texture=texture)
    background_sprite.rect = pygame2.Rect(0, 0, 2, 2)

    texture = loader('players', 'Green', 'alienGreen_walk1.png')
    player_sprite = renderer.create_sprite(texture=texture)
    player_sprite.rect = pygame2.Rect(0, 0, .25, .5)

    app.clock.schedule(update, desired_fps, repeat=True)

    # this will start the application and will exit when window is closed
    app.run()


if __name__ == '__main__':
    main()
