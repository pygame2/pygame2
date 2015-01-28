import pyglet
import collections
from . import InputProviderBase


class KeyStateHandler:
    def __init__(self):
        self.keys = collections.OrderedDict()
        for symbol in pyglet.window.key._key_names.keys():
            self.keys[symbol] = False

    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False


class PygletKeyboardProvider(InputProviderBase):
    def __init__(self):
        # global _initia
        # if not _initialized:
        #     win = pygame2.display.get_window()
        #     kbd = KeyStateHandler()
        #     win.push_handlers(kbd)
        #     _keyhandler = kbd
        #     _initialized = True
        pass

    def get_focused(self):
        """true if the display is receiving keyboard input from the system

        :return: bool
        """
        raise NotImplementedError


    def get_pressed(self):
        """get the state of all keyboard buttons

        :return: bools
        """
        # return _keyhandler.keys.values()
        raise NotImplementedError

    def get_mods(self):
        """determine which modifier keys are being held

        :return: int
        """
        raise NotImplementedError

    def set_mods(self):
        """temporarily set which modifier keys are pressed
        """
        raise NotImplementedError

    def set_repeat(self):
        raise NotImplementedError

    def get_repeat(self):
        raise NotImplementedError

    def name(self, key):
        """get the name of a key identifier

        :param key: int of key code
        :return: str of descriptive key name
        """
        raise NotImplementedError

