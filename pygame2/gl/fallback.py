# import gl
# from . import internal
#
#
# class VAO:
#     counter = 1
#     mem = {}
#
#
# def glGenVertexArrays(count, ptrs):
#     for i in range(count):
#         vid = VAO.counter
#         VAO.mem[vid] = {}
#         VAO.counter += 1
#         ptrs[i] = vid
#
#
# def glBindVertexArray(vid):
#     pass
#
#
# def glBindFragDataLocation(program, locid, name):
#     pass
#
#
# def glGenerateMipmap(target):
#     # do not generate mipmaps - instead, turn off mipmap setting
#     gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
#                        gl.GL_NEAREST)
