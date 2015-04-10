from pygame2.core import core_modules

__all__ = ('load', )


# declare audio providers
# core_modules['audio'] = ('audio_pysdl2', 'audio_fmod')
core_modules['audio'] = ()


def load(filename):
    """

    :param filename: filename of audio file to load
    :return: pygame2.audio.Sound object
    """
    from pygame2.core import core_providers

    snd = None
    for provider in core_providers['audio']:
        try:
            snd = provider.SoundLoader.load(filename)
            break
        except:
            raise

    return snd
