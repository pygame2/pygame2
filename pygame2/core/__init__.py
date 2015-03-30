"""
do magic here to load the best available loaders for the pygame2 core
"""
core_modules = dict()
core_providers = dict()

import logging

from . import audio
from . import image
from . import platform


logger = logging.getLogger('pygame2.core')


def load_modules():
    import importlib

    def iterate_providers():
        for provider in providers:
            path = 'pygame2.core.{}.{}'.format(name, provider)
            # TODO: change warn to debug
            try:
                yield importlib.import_module(path)
                logger.warn("imported: %s", path)
            except ImportError:
                logger.warn('cannot import %s', path)
                pass

    for name in list(core_modules.keys()):
        providers = core_modules[name]
        core_providers[name] = list(iterate_providers())


load_modules()
