# a collection of classes to help with managing the lifetime of GL resources

from __future__ import (print_function, division, absolute_import)

import threading
import traceback

from .corearb import *
from .corearb import _symmetric_managers

__all__ = [
    'glShader',
    'glProgram',
    'glVertexArrays', 'glVertexArray',
    'glBuffers', 'glBuffer',
    'glTextures', 'glTexture',
    'glSamplers', 'glSampler',
    'glQueries', 'glQuery',
    'glTransformFeedbacks', 'glTransformFeedback',
    'glProgramPipelines', 'glProgramPipeline',
    'glFramebuffers', 'glFramebuffer',
    'glRenderbuffers', 'glRenderbuffer',
    'GLGC',
]

################################################################################


class GLGC(object):
    """
    Since it is not guaranteed that __del__ will be called in the thread
    that instantiated the resource, all managed objects defer resource
    destruction to the threads GLGC. For this to work, GLGC.initialize()
    must be called once in each GL thread before creating the first
    context.

    GLGC.collect() must then be called in regular intervals (e.g. between
    frames) to free GL objects that may have been released inbetween.
    """

    local_storage = threading.local()

    @classmethod
    def collect(cls):
        local_storage = cls.local_storage
        garbage = local_storage.garbage
        local_storage.garbage = []
        count = len(garbage)
        for func, id_, info in garbage:
            func(id_)
        return count

    @classmethod
    def get_garbage(cls):
        return cls.local_storage.garbage

    @classmethod
    def initialize(cls):
        local_storage = cls.local_storage
        assert not hasattr(local_storage, 'garbage')
        local_storage.garbage = []
        local_storage.traps = set()

    @classmethod
    def trap(cls, info, id_):
        local_storage = cls.local_storage
        local_storage.traps.add((info, id_))

    @classmethod
    def is_trapped(cls, info, id_):
        return (info, id_) in cls.local_storage.traps

    @classmethod
    def check_trap(cls, action, obj, info, id_):
        if cls.is_trapped(info, id_):
            print(action, obj, info, id_)
            traceback.print_stack()

    @classmethod
    def tag(cls, obj, destructor, id_, info):
        cls.check_trap('GLGC TAGGED:', obj, info, id_)
        cls.local_storage.garbage.append((destructor, id_, info))

################################################################################


def build_class_r2r(name, create_func, delete_func):
    """build class for single resource functions"""

    def __init__(self, *args):
        self._id = create_func(*args)
        GLGC.check_trap('GLGC NEW:', self, name, self._id)

    def __int__(self):
        return self._id

    def Delete(self):
        if self._id is None: return
        GLGC.tag(self, delete_func, self._id, name)
        self._id = None

    def __del__(self):
        self.Delete()

    return type(name, (), dict(
        __init__=__init__,
        __int__=__int__,
        Delete=Delete,
        __del__=__del__,
    ))


def build_class_rr2r(name, create_func, delete_func):
    """build single class for array resource functions"""

    def __init__(self):
        self._id = create_func(1)[0]
        GLGC.check_trap('GLGC NEW:', self, name, (self._id,))

    def __int__(self):
        return self._id

    def Delete(self):
        if self._id is None: return
        GLGC.tag(self, delete_func, (self._id,), name)
        self._id = None

    def __del__(self):
        self.Delete()

    return type(name, (), dict(
        __init__=__init__,
        __int__=__int__,
        Delete=Delete,
        __del__=__del__,
    ))


def build_class_rr2rr(name, create_func, delete_func):
    """build array class for array resource functions"""

    def __init__(self, count):
        self._ids = tuple(create_func(count))
        GLGC.check_trap('GLGC NEW:', self, name, self._ids)

    def __iter__(self):
        return iter(self._ids)

    def __getitem__(self, index):
        return self._ids[index]

    def Delete(self):
        if self._ids is None: return
        GLGC.tag(self, delete_func, self._ids, name)
        self._ids = None

    def __del__(self):
        self.Delete()

    return type(name, (), dict(
        __init__=__init__,
        __iter__=__iter__,
        __getitem__=__getitem__,
        Delete=Delete,
        __del__=__del__,
    ))


################################################################################

def build_classes(ns):
    for plural, singular in _symmetric_managers:
        genfunc = ns['glGen' + plural]
        delfunc = ns['glDelete' + plural]
        clsname = 'gl' + singular
        ns[clsname] = build_class_rr2r(clsname, genfunc, delfunc)
        # __all__.append(clsname)
        clsname = 'gl' + plural
        ns[clsname] = build_class_rr2rr(clsname, genfunc, delfunc)
        #__all__.append(clsname)


build_classes(locals())

################################################################################

glShader = build_class_r2r('glShader', glCreateShader, glDeleteShader)
glProgram = build_class_r2r('glProgram', glCreateProgram, glDeleteProgram)

################################################################################
