from __future__ import (print_function, division, absolute_import)

from cffi import FFI  # @UnresolvedImport
import sys
import traceback
import os
import logging

log = logging.getLogger('pyopengl')

__all__ = [
    '_ffi',
    'load_lib',
    'lookup',
    'check_error',
    'guard',
    'update_defs',
    'GLError',
]


class GLError(Exception):
    pass


_ffi = FFI()
_LIB = None

IS_WIN32 = sys.platform == 'win32'
IS_DARWIN = sys.platform == 'darwin'

RAISE_ON_ERROR = True
CHECK_LAST_ERROR = False
VERBOSE_CALLS = False

DARWIN_LIB_PATH = "/System/Library/Frameworks/OpenGL.framework/Libraries"

WIN32_WGL_CDEFS = """
void *wglGetCurrentContext(void);
void *wglGetProcAddress(const char *);
"""


def find_win32_library(name):
    WIN32_SEARCH_PATH = os.environ.get('PATH', '').split(os.pathsep)
    WIN32_SEARCH_PATH.insert(0, r'c:\windows\system32')
    filename = name + '.dll'
    for path in WIN32_SEARCH_PATH:
        fullpath = os.path.join(path, filename)
        if os.path.isfile(fullpath):
            return fullpath
    return name


def load_lib(cdefs):
    global _LIB

    # import time
    #t = time.time()
    if IS_WIN32:
        libname = find_win32_library('opengl32')
        cdefs += WIN32_WGL_CDEFS
    elif IS_DARWIN:
        libname = os.path.join(DARWIN_LIB_PATH, "libGL.dylib")
    else:
        libname = 'GL'
    _ffi.cdef(cdefs)
    #print("GL cdefs loaded in {0}s".format(time.time() - t))
    _LIB = _ffi.dlopen(libname)
    if IS_WIN32:
        # make sure these attributes exist
        assert _LIB.wglGetProcAddress
        assert _LIB.wglGetCurrentContext
    return _LIB


def wrapstr(result):
    if result:
        return _ffi.string(result)
    return None


def wrap_retstr(func):
    def wrapper(*argv):
        return wrapstr(func(*argv))

    return wrapper


def wrap_gen(func):
    def wrapper(count):
        ids = _ffi.new('GLuint[]', [0] * count)
        func(count, ids)
        return [int(i) for i in ids]

    return wrapper


def wrap_del(func):
    def wrapper(ids):
        func(len(ids), ids)

    return wrapper


class Thunk(object):
    # on windows, some functions are only available after the GL context
    # has been loaded. therefore, defer the function import until the
    # actual call, when the context is likely to be valid.

    glflush = None
    glfinish = None

    def __init__(self, name):
        self.name = name
        self.func = self._thunk
        if name == 'glFlush':
            Thunk.glflush = self
        if name == 'glFinish':
            Thunk.glfinish = self

    def __bool__(self):
        return True if self._resolve() else False

    def _resolve(self):
        assert _LIB.wglGetCurrentContext(), 'you must be in a valid GL context'
        func = _LIB.wglGetProcAddress(bytes(self.name, "utf-8"))
        if not func:
            from . import fallback

            if hasattr(fallback, self.name):
                print('warning: falling back to emulated {0}'.format(self.name))
                return getattr(fallback, self.name)
            return None
        # attempt to cast to functype
        functypename = 'PFN' + self.name.upper() + 'PROC'
        return _ffi.cast(functypename, func)

    def _thunk(self, *args, **kargs):
        return self.c_function(*args, **kargs)

    @property
    def c_function(self):
        func = self.func
        if func == self._thunk:
            func = self._resolve()
            if func is None:
                raise NotImplementedError(
                    'unable to import function: {0}'.format(self.name))
            self.func = func
        return func

    if VERBOSE_CALLS:
        def __call__(self, *args, **kargs):
            print(self.name, *args, **kargs)
            return self.func(*args, **kargs)
    else:
        def __call__(self, *args, **kargs):
            return self.func(*args, **kargs)


if IS_WIN32:
    def lookup(name):
        if hasattr(_LIB, name):
            return getattr(_LIB, name)
        return Thunk(name)
else:
    def lookup(name):
        if hasattr(_LIB, name):
            return getattr(_LIB, name)
        # TODO: Fix this
        # log.warn("GL warning: function", name, "missing.")
        return None

_ERROR_DESC = {}


def check_error():
    error = _LIB.glGetError()
    if error == 0:
        return
    if RAISE_ON_ERROR:
        raise GLError(_ERROR_DESC.get(error, repr(error)))


def guard(func):
    if isinstance(func, Thunk):
        return func
    if not func:
        return None
    if CHECK_LAST_ERROR:
        def call(*args, **kargs):
            result = func(*args, **kargs)
            check_error()
            return result

        return call
    return func


def update_defs(m):
    global _ERROR_DESC
    _ERROR_DESC = {
        m['GL_NO_ERROR']: "GL_NO_ERROR: No error has been recorded.",
        m[
            'GL_INVALID_ENUM']: "GL_INVALID_ENUM: An unacceptable value is specified for an enumerated argument.",
        m[
            'GL_INVALID_VALUE']: "GL_INVALID_VALUE: A numeric argument is out of range.",
        m[
            'GL_INVALID_OPERATION']: "GL_INVALID_OPERATION: The specified operation is not allowed in the current state.",
        m[
            'GL_STACK_OVERFLOW']: "GL_STACK_OVERFLOW: This command would cause a stack overflow.",
        m[
            'GL_STACK_UNDERFLOW']: "GL_STACK_UNDERFLOW: This command would cause a stack underflow.",
        m[
            'GL_OUT_OF_MEMORY']: "GL_OUT_OF_MEMORY: There is not enough memory left to execute the command.",
    }
