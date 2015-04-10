from pygame2.core import core_modules

__all__ = ['create_renderer', 'NoGraphicsBackend']


# declare audio providers
core_modules['graphics'] = ('graphics_opengl', )


class NoGraphicsBackend(Exception):
    pass


def get_backend():
    # TODO: actual other graphics loading
    pass


def create_renderer():
    from pygame2.core import core_providers

    renderer = None
    for provider in core_providers['graphics']:
        try:
            renderer = provider.SpriteRenderer()
            break
        except:
            raise

    if renderer is None:
        raise NoGraphicsBackend

    return renderer
