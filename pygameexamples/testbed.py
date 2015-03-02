"""
this is a testbed for the opengl operations of pygame2

the general goal is to create new useful functions for pygame2
this testbed is meant to code first, then refactor useful code
into pygame2.  mostly, things will be moved into pygame2.graphics.
"""
import os

import pygame2
from pygame2.graphics import *

import numpy
import OpenGL

OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *

# http://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_02


def do_tex_coords():
    # no need to flip loaded images
    # the stuff below needs a home
    quad_texcoords = numpy.array([
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 1.0,
    ], dtype='float32')

    vbo = VertexBufferObject(quad_texcoords, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
    return vbo


def load_texture(flip_y=False):
    path = os.path.join('resources', 'pygame2.png')

    # pillow image loading
    from PIL import Image
    image = Image.open(path)
    width, height = image.size
    image = image.convert("RGBA")
    if flip_y:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    data = image.tostring('raw', 'RGBA', 0, -1)

    # pygame2 image loading
    # image = pygame2.core.image.load(path)
    # data = str(image.convert())
    # data = numpy.fromstring(data, dtype='uint8')

    texture = Texture(width, height, data)
    return texture


def main():
    size = 800, 800
    window = pygame2.core.platform.create_window(size=size)
    assert(get_opengl_version()[0] > 3)

    program_id = create_program()
    texture = load_texture()
    tex_coords = do_tex_coords()

    group = pygame2.group.SpriteGroup(program_id, texture)
    sprite = pygame2.sprite.Sprite()

    # hack for now
    attr = group.batch.attr
    group.batch._attr[attr['texcoord']] = tex_coords
    group.batch._attr[attr['coord2d']] = sprite.vbo

    def on_draw(*args, **kwargs):
        glClearColor(.98, .98, .98, 1.)
        glClear(GL_COLOR_BUFFER_BIT)
        group.draw()

    window.bind('on_draw', on_draw)

    # just a test, of course
    def update(dt):
        sprite.rotation += 10 * dt
        sprite.update_vbo()
        group.batch._attr[attr['coord2d']] = sprite.vbo

    app = pygame2.app.App()
    app.clock.schedule(update, 1/50., repeat=True)
    app.run(window)


if __name__ == '__main__':
    main()
