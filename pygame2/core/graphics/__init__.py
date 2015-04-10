from pygame2.core import core_modules

__all__ = ('load', )


# declare audio providers
core_modules['graphics'] = ('graphics_opengl', )


def get_backend():
    # TODO: actual other graphics loading

    pass


def create_renderer():
    from pygame2.core import core_providers

    renderer = None
    for provider in core_providers['graphics']:
        try:
            renderer = provider.SpriteGroup()
            break
        except:
            raise

    if renderer is None:
        raise Exception

    return renderer
