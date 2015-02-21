# # code generator - only required at build time
# from __future__ import (print_function, division, absolute_import)
#
# import os
# from autobind import AutoBind
#
# THISDIR = os.path.dirname(__file__)
#
# POST_TEMPLATE = """
# update_defs(locals())
# """
#
# autobind = AutoBind(options=dict(
#     CDEF_PATH=os.path.join(THISDIR, '..', 'gl_defs'),
#     CDEF_FILES=[
#         'glcorearb.h',
#     ],
#     DEFINES_BLACKLIST=[
#         'APIENTRY',
#         'APIENTRYP',
#         'GLAPI',
#     ],
#     DEFINES=[
#         'GLCOREARB_PROTOTYPES',
#         # excluded extensions
#         'GL_ARB_vertex_attrib_binding',
#         'GL_KHR_debug',
#         'GL_ARB_texture_storage_multisample',
#         'GL_ARB_invalidate_subdata',
#         'GL_ARB_program_interface_query',
#         'GL_ARB_framebuffer_no_attachments',
#         'GL_ARB_copy_image',
#         'GL_ARB_clear_buffer_object',
#         'GL_ARB_shader_storage_buffer_object',
#         'GL_ARB_compute_shader',
#         'GL_ARB_multi_draw_indirect',
#         'GL_ARB_texture_buffer_range',
#         'GL_ARB_texture_view',
#         'GL_ARB_cl_event',
#         'GL_ARB_internalformat_query2',
#     ],
#     PRIVATE_SYMBOLS=[
#         'glShaderSource',
#     ],
#     AUTOCHECK_BLACKLIST=[
#         'glGetError',
#     ],
#     REPLACES=[
#         ('APIENTRYP', '*'),
#         ('APIENTRY', ''),
#         ('GLAPI', ''),
#     ],
#     LIBNAME='GL',
#     AUTOMANGLE=True,
#     PYPREDEFS=os.path.join(THISDIR, '..', 'predefs', 'gl.pypredef'),
#     OUTMODULE=os.path.join(THISDIR, '_corearb.py'),
#     GENPOSTFIX=POST_TEMPLATE,
# ))
#
# ################################################################################
#
# if __name__ == '__main__':
#     autobind.build()
