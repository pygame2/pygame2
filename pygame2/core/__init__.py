"""
do magic here to load the best available loaders for the pygame2 core
"""
core_modules = dict()
core_providers = dict()


from . import image


import logging

logger = logging.getLogger('pygame2.core')


def load_modules():
    import importlib

    def iterate_providers():
        for provider in providers:
            path = 'pygame2.core.{}.{}'.format(name, provider)
            logger.debug("imported: %s", path)
            try:
                yield importlib.import_module(path)
            except:
                logger.debug('cannot import {}'.format(path))

    for name, providers in core_modules.items():
        core_providers[name] = list(iterate_providers())


load_modules()
