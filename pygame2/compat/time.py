from __future__ import absolute_import
import time

__all__ = ('Clock', 'get_ticks', 'wait', 'delay', 'set_timer')


# Conversions
s2ms = lambda s: s * 1000.0
ms2s = lambda ms: ms / 1000.0

s2fps = lambda s: 1.0 / s
fps2s = lambda fps: 1.0 / fps

ms2fps = lambda ms: s2fps(ms2s(ms))
fps2ms = lambda fps: s2ms(fps2s(fps))


class Clock(object):
    def __init__(self):
        self._last_10_calls = [time.clock()] * 10
        self._last_cur_call = 0

    def tick(self, framerate=0):
        cur_time = time.clock()
        if framerate > 0:
            wait(fps2ms(framerate))

        ret = cur_time - self._last_10_calls[self._last_cur_call]
        self._last_cur_call = (self._last_cur_call + 1) % 10
        self._last_10_calls[self._last_cur_call] = cur_time
        return ret

    def tick_busy_loop(self, framerate=0):
        cur_time = time.clock()
        if framerate > 0:
            delay(fps2ms(framerate))

        ret = cur_time - self._last_10_calls[self._last_cur_call]
        self._last_cur_call = (self._last_cur_call + 1) % 10
        self._last_10_calls[self._last_cur_call] = cur_time
        return ret

    def get_time(self):
        return s2ms(self._last_10_calls[((self._last_cur_call - 1) % 10)] -
                    self._last_10_calls[self._last_cur_call])

    def get_rawtime(self):
        raise NotImplementedError

    def get_fps(self):
        avg = 0
        for i in range(0, 10):
            avg += i
        return s2fps(avg / 10)


def get_ticks():
    pass


def wait(ms):
    time.sleep(ms2s(ms))


def delay(ms):
    t1 = time.clock()
    t2 = time.clock()
    while ms > (t2 - t1):
        t2 = time.clock()


def set_timer(eventid, ms):
    pass
