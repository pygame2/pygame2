"""
Where pygame made sounds and music different, pygame2
unifies them. there is no confusing arbitrary difference
between 'sounds', and 'music'.

instead, the difference is a much more palpable
'stored in memory' or 'streamed'.

API for determining each is in progress
"""
from pygame2.event import EventDispatcher


class SoundBase(EventDispatcher):
    """Base for objects that play sounds/music
    """
    _source = None
    _volume = 1.0
    _state = None
    _loop = None
    _position = None
    _length = None

    @property
    def source(self):
        return self._source

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if not self._volume == value:
            self._volume = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        pass

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        raise NotImplementedError('abstract')

    @property
    def length(self):
        raise NotImplementedError('abstract')

    def load(self):
        """Load the file into memory."""
        raise NotImplementedError('abstract')

    def unload(self):
        """Unload the file from memory."""
        raise NotImplementedError('abstract')

    def play(self):
        """Play the file."""
        self.state = 'play'
        self.broadcast('on_play')

    def stop(self):
        """Stop playback."""
        self.state = 'stop'
        self.broadcast('on_stop')

    def seek(self, position):
        """Go to the <position> (in seconds)."""
        raise NotImplementedError('abstract')
