from __future__ import (print_function, division, absolute_import)

import collections
from ._corearb import *
from .internal import wrap_retstr, wrap_gen, wrap_del

################################################################################

GL_TYPES = [
    'GLenum',
    'GLboolean',
    'GLbitfield',
    'GLbyte',
    'GLshort',
    'GLint',
    'GLsizei',
    'GLubyte',
    'GLushort',
    'GLuint',
    'GLhalf',
    'GLfloat',
    'GLclampf',
    'GLdouble',
    'GLclampd',
    'GLvoid',
]

for typename in GL_TYPES:
    locals()[typename] = typename

GL_TYPE_ID_TO_TYPE = {
    GL_BYTE: GLbyte,
    GL_UNSIGNED_BYTE: GLubyte,
    GL_SHORT: GLshort,
    GL_UNSIGNED_SHORT: GLushort,
    GL_INT: GLint,
    GL_UNSIGNED_INT: GLuint,
    GL_FLOAT: GLfloat,
    GL_DOUBLE: GLdouble,
}

GL_FORMAT_TO_COUNT = {
    GL_RED: 1,
    GL_RG: 2,
    GL_RGB: 3,
    GL_RGBA: 4
}

################################################################################

def _cstr(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return _ffi.new('char[]', data)


def _array(type_, data):
    return _ffi.new(type_ + '[]', data)


def _flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el,
                                                                   str):
            for sub in _flatten(el):
                yield sub
        else:
            yield el


################################################################################

def new_gl_buffer(typeid, count):
    return _ffi.new('{0}[{1}]'.format(
        GL_TYPE_ID_TO_TYPE[typeid], count))


def glDrawBuffers(bufs):
    _glDrawBuffers(len(bufs), _array('GLenum', bufs))


def glShaderSource(shader, sources):
    sources = [_cstr(source) for source in sources]
    _glShaderSource(shader, len(sources), sources, _ffi.NULL)


def glGetShaderiv(shader, pname):
    params = _ffi.new('GLint *')
    _glGetShaderiv(shader, pname, params)
    return params[0]


def glGetShaderInfoLog(shader):
    maxLength = glGetShaderiv(shader, GL_INFO_LOG_LENGTH)
    length = _ffi.new('GLsizei *')
    infoLog = _ffi.new('char[]', maxLength)
    _glGetShaderInfoLog(shader, maxLength, length, infoLog)
    return _ffi.string(infoLog)


def glGetShaderSource(shader):
    maxLength = glGetShaderiv(shader, GL_SHADER_SOURCE_LENGTH)
    length = _ffi.new('GLsizei *')
    source = _ffi.new('char[]', maxLength)
    _glGetShaderSource(shader, maxLength, length, source)
    return _ffi.string(source)


def glGetProgramiv(program, pname):
    params = _ffi.new('GLint *')
    _glGetProgramiv(program, pname, params)
    return params[0]


def glGetProgramInfoLog(program):
    maxLength = glGetProgramiv(program, GL_INFO_LOG_LENGTH)
    length = _ffi.new('GLsizei *')
    infoLog = _ffi.new('char[{0}]'.format(maxLength))
    _glGetProgramInfoLog(program, maxLength, length, infoLog)
    return _ffi.string(infoLog)


def glGetActiveUniformName(program, index):
    bufsize = glGetActiveUniformsiv(program, [index], GL_UNIFORM_NAME_LENGTH)[0]
    name = _ffi.new('char[]', bufsize)
    _glGetActiveUniformName(program, index, bufsize, _ffi.NULL, name)
    return _ffi.string(name)


def glGetActiveUniform(program, index):
    bufsize = glGetProgramiv(program, GL_ACTIVE_UNIFORM_MAX_LENGTH)
    size = _ffi.new('GLint *')
    type_ = _ffi.new('GLenum *')
    name = _ffi.new('char[]', bufsize)
    _glGetActiveUniform(program, index, bufsize, _ffi.NULL,
                        size, type_, name)
    return size[0], type_[0], _ffi.string(name)


def glGetActiveUniformsiv(program, indices, pname, pcount=1):
    count = len(indices)
    params = _ffi.new('GLint[]', count * pcount)
    _glGetActiveUniformsiv(program, count, indices, pname, params)
    return params


def glGetActiveUniformBlockiv(program, index, pname, pcount):
    params = _ffi.new('GLint[]', pcount)
    _glGetActiveUniformBlockiv(program, index, pname, params)
    return params


def glGetActiveUniformBlockName(program, index):
    bufsize = glGetActiveUniformBlockiv(program, index,
                                        GL_UNIFORM_BLOCK_NAME_LENGTH, 1)[0]
    name = _ffi.new('char[]', bufsize)
    _glGetActiveUniformBlockName(program, index, bufsize, _ffi.NULL, name)
    return _ffi.string(name)


def glGetAttribLocation(program, name):
    return _glGetAttribLocation(program, _cstr(name))


def glGetBufferParameteriv(target, value):
    data = _ffi.new('GLint *')
    _glGetBufferParameteriv(target, value, data)
    return data[0]


def glGetBufferSubData(target, offset, size, type_):
    bytesize = _ffi.sizeof(type_)
    ptr = _array(type_, size)
    _glGetBufferSubData(target, offset * bytesize, _ffi.sizeof(ptr), ptr)
    return ptr


def glGetFramebufferAttachmentParameteriv(target, attachment, pname):
    data = _ffi.new('GLint *')
    _glGetFramebufferAttachmentParameteriv(target, attachment, pname, data)
    return data[0]


def glBufferData(target, type_, data, usage):
    if data is None:
        ptr = _ffi.NULL
    elif isinstance(data, CData):
        ptr = data
    else:
        ptr = _array(type_, data)
    if isinstance(type_, int):
        size = type_
    elif data is None:
        size = _ffi.sizeof(type_)
    else:
        size = _ffi.sizeof(ptr)
    _glBufferData(target, size, ptr, usage)
    return ptr

# providing our own until ffi has it
CData = type(_ffi.cast("int", 0))
CType = type(_ffi.typeof("int"))


def glBufferSubData(target, type_, offset, data):
    if isinstance(data, CData):
        ptr = data
    else:
        ptr = _array(type_, data)
    if isinstance(type_, int):
        size = type_
    else:
        offset *= _ffi.sizeof(type_)
        size = _ffi.sizeof(ptr)
    _glBufferSubData(target, offset, size, ptr)
    return ptr


def glVertexAttribPointer(index, size, typeid, normalized, stride, data):
    if isinstance(data, int):
        ptr = _ffi.cast('GLvoid *', data)
    elif data:
        type_ = GL_TYPE_ID_TO_TYPE[typeid]
        ptr = _array(type_, data)
    else:
        ptr = _ffi.NULL
    _glVertexAttribPointer(index, size, typeid, normalized, stride, ptr)
    return ptr


def glDrawElements(mode, typeid, data):
    if isinstance(data, int):
        _glDrawElements(mode, data, typeid, _ffi.NULL)
    else:
        type_ = GL_TYPE_ID_TO_TYPE[typeid]
        ptr = _array(type_, data)
        _glDrawElements(mode, len(data), typeid, ptr)


def glGetUniformfv(program, location, params):
    if isinstance(params, int):
        params = _ffi.new('float[]', params)
        _glGetUniformfv(program, location, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetUniformfv(program, location, params)
        return params[0]


def glGetUniformiv(program, location, params):
    if isinstance(params, int):
        params = _ffi.new('int[]', params)
        _glGetUniformiv(program, location, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetUniformiv(program, location, params)
        return params[0]


def glGetUniformuiv(program, location, params):
    if isinstance(params, int):
        params = _ffi.new('unsigned int[]', params)
        _glGetUniformuiv(program, location, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetUniformuiv(program, location, params)
        return params[0]


def glGetUniformdv(program, location, params):
    if isinstance(params, int):
        params = _ffi.new('double[]', params)
        _glGetUniformdv(program, location, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetUniformdv(program, location, params)
        return params[0]


def glUniform1fv(location, values):
    _glUniform1fv(location, len(values), values)


def glUniform2fv(location, values):
    assert (len(values) % 2) == 0
    _glUniform2fv(location, len(values) // 2, values)


def glUniform3fv(location, values):
    assert (len(values) % 3) == 0
    _glUniform3fv(location, len(values) // 3, values)


def glUniform4fv(location, values):
    assert (len(values) % 4) == 0
    _glUniform4fv(location, len(values) // 4, values)


def glUniform1iv(location, values):
    _glUniform1iv(location, len(values), values)


def glUniform2iv(location, values):
    assert (len(values) % 2) == 0
    _glUniform2iv(location, len(values) // 2, values)


def glUniform3iv(location, values):
    assert (len(values) % 3) == 0
    _glUniform3iv(location, len(values) // 3, values)


def glUniform4iv(location, values):
    assert (len(values) % 4) == 0
    _glUniform4iv(location, len(values) // 4, values)


def glUniformMatrix3fv(location, transpose, values):
    assert (len(values) % 9) == 0
    # print(location, len(data)//16, transpose, data)
    _glUniformMatrix3fv(location, len(values) // 9, transpose, values)


def glUniformMatrix4fv(location, transpose, values):
    assert (len(values) % 16) == 0
    # print(location, len(data)//16, transpose, data)
    _glUniformMatrix4fv(location, len(values) // 16, transpose, values)


glGetUniformLocation = _glGetUniformLocation


def _wrap_texture_data(type, data):
    if isinstance(data, CData):
        return data
    elif isinstance(data, (tuple, list)):
        return _array(GL_TYPE_ID_TO_TYPE[type], data)
    elif data is None:
        return _ffi.NULL
    else:
        return _ffi.new('char[]', data)


def glTexImage1D(target, level, internalFormat, width, border, format, type,
                 data):
    ptr = _wrap_texture_data(type, data)
    _glTexImage1D(target, level, internalFormat, width, border, format, type,
                  ptr)


def glTexImage2D(target, level, internalFormat, width, height, border, format,
                 type, data):
    ptr = _wrap_texture_data(type, data)
    _glTexImage2D(target, level, internalFormat, width, height, border, format,
                  type, ptr)


def glTexImage3D(target, level, internalFormat, width, height, depth, border,
                 format, type, data):
    ptr = _wrap_texture_data(type, data)
    _glTexImage3D(target, level, internalFormat, width, height, depth, border,
                  format, type, ptr)


def glTexSubImage1D(target, level, xoffset, width, format, type, data):
    ptr = _wrap_texture_data(type, data)
    _glTexSubImage1D(target, level, xoffset, width, format, type, ptr)


def glTexSubImage2D(target, level, xoffset, yoffset, width, height, format,
                    type, data):
    ptr = _wrap_texture_data(type, data)
    _glTexSubImage2D(target, level, xoffset, yoffset, width, height, format,
                     type, ptr)


def glTexSubImage3D(target, level, xoffset, yoffset, zoffset, width, height,
                    depth, format, type, data):
    ptr = _wrap_texture_data(type, data)
    _glTexSubImage3D(target, level, xoffset, yoffset, zoffset, width, height,
                     depth, format, type, ptr)


def glTexParameterfv(target, pname, values):
    _glTexParameterfv(target, pname, values)


def glReadPixels(x, y, width, height, format, type, data=None):
    if data is None:
        ptr = _array(GL_TYPE_ID_TO_TYPE[type],
                     (width * height * GL_FORMAT_TO_COUNT[format]))
    elif isinstance(data, int):
        ptr = _ffi.cast('void*', data)
    _glReadPixels(x, y, width, height, format, type, ptr)
    return ptr


def glBindFragDataLocation(program, colorNumber, name):
    _glBindFragDataLocation(program, colorNumber, _cstr(name))


def glBindAttribLocation(program, index, name):
    _glBindAttribLocation(program, index, _cstr(name))


def unwrap_ctype(obj):
    if hasattr(obj, '_ctype_'):
        return obj._ctype_
    return obj


def glGetBooleanv(pname, params):
    if isinstance(params, int):
        params = _ffi.new('int[]', params)
        _glGetBooleanv(pname, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetBooleanv(pname, params)
        return params[0]


def glGetDoublev(pname, params):
    if isinstance(params, int):
        params = _ffi.new('double[]', params)
        _glGetDoublev(pname, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetDoublev(pname, params)
        return params[0]


def glGetFloatv(pname, params):
    if isinstance(params, int):
        params = _ffi.new('float[]', params)
        _glGetFloatv(pname, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetFloatv(pname, params)
        return params[0]


def glGetMultisamplefv(pname, index):
    params = _ffi.new('float[2]')
    _glGetMultisamplefv(pname, index, params)
    return list(params)


def glGetIntegerv(pname, params):
    if isinstance(params, int):
        params = _ffi.new('int[]', params)
        _glGetIntegerv(pname, params)
        return list(params)
    else:
        params = unwrap_ctype(params)
        _glGetIntegerv(pname, params)
        return params[0]


def glGetQueryObjectiv(query, pname):
    params = _ffi.new('GLint *')
    _glGetQueryObjectiv(query, pname, params)
    return params[0]


def glGetQueryObjectuiv(query, pname):
    params = _ffi.new('GLuint *')
    _glGetQueryObjectuiv(query, pname, params)
    return params[0]


def glTransformFeedbackVaryings(program, varyings, buffermode):
    if varyings:
        varyings = [_ffi.new('char []', s) for s in varyings]
        varyings = _ffi.new('char *[]', varyings)
        count = len(varyings)
    else:
        count = 0
        varyings = _ffi.NULL
    _glTransformFeedbackVaryings(program, count, varyings, buffermode)


glMapBuffer = _glMapBuffer
glMapBufferRange = _glMapBufferRange


class callbacks:
    _debug_message_callback = None


def glDebugMessageCallbackARB(callback):
    @_ffi.callback('GLDEBUGPROCARB')
    def callback_wrapper(source, type_, id_, severity, length, message,
                         userparam):
        msg = _ffi.string(message)
        callback(source, type_, id_, severity, msg)

    callbacks._debug_message_callback = callback_wrapper
    _glDebugMessageCallbackARB(callback_wrapper, _ffi.NULL)


glFenceSync = _glFenceSync
glClientWaitSync = _glClientWaitSync
glWaitSync = _glWaitSync
glDeleteSync = _glDeleteSync

glDrawElementsInstanced = _glDrawElementsInstanced

################################################################################

_symmetric_managers = [
    ('VertexArrays', 'VertexArray'),
    ('Buffers', 'Buffer'),
    ('Textures', 'Texture'),
    ('Samplers', 'Sampler'),
    ('Queries', 'Query'),
    ('TransformFeedbacks', 'TransformFeedback'),
    ('ProgramPipelines', 'ProgramPipeline'),
    ('Framebuffers', 'Framebuffer'),
    ('Renderbuffers', 'Renderbuffer')
]

_wrap_methods = {
    wrap_retstr: [
        'glGetString',
        'glGetStringi',
    ],
    wrap_gen: [
    ],
    wrap_del: [
    ],
}


def build_wrappers(ns):
    wrapgenlist = _wrap_methods[wrap_gen]
    wrapdellist = _wrap_methods[wrap_del]
    for plural, singular in _symmetric_managers:
        wrapgenlist.append('glGen' + plural)
        wrapdellist.append('glDelete' + plural)

    for method, names in list(_wrap_methods.items()):
        for name in names:
            ns[name] = method(ns['_' + name])


build_wrappers(locals())
del _wrap_methods

################################################################################

# add wrapped functions
_module_names = set(locals().keys())


def get_mangled_names():
    for name in UNMANGLED_EXPORTS:
        mangled_name = name.lstrip('_')
        if mangled_name in _module_names:
            yield mangled_name
        else:
            yield name


__all__ = EXPORTS + list(get_mangled_names()) + GL_TYPES + [
    'GL_TYPE_ID_TO_TYPE',
    'new_gl_buffer',
]
del _module_names

################################################################################
