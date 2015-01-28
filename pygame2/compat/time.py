import time

__all__ = ['Clock', 'get_ticks', 'wait', 'delay', 'set_timer']


# Conversions
s2ms = lambda s: s * 1000.
ms2s = lambda ms: ms / 1000.0

s2fps = lambda s: 1.0 / s
fps2s = lambda fps: 1.0 / fps

ms2fps = lambda ms: s2fps(ms2s(ms))
fps2ms = lambda fps: s2ms(fps2s(fps))


# Pygame2 Clock class
class Clock:
    def __init__(self):
        self._Last10Calls = [time.clock()] * 10
        self._LastCurCall = 0

    def tick(self, framerate=0):
        CurTime = time.clock()
        if (framerate > 0):
            wait(fps2ms(framerate))

        ret = CurTime - self._Last10Calls[self._LastCurCall]
        self._LastCurCall = (self._LastCurCall + 1) % 10
        self._Last10Calls[self._LastCurCall] = CurTime
        return ret

    def tick_busy_loop(self, framerate=0):
        CurTime = time.clock()
        if (framerate > 0):
            delay(fps2ms(framerate))

        ret = CurTime - self._Last10Calls[self._LastCurCall]
        self._LastCurCall = (self._LastCurCall + 1) % 10
        self._Last10Calls[self._LastCurCall] = CurTime
        return ret

    def get_time(self):
        return s2ms(self._Last10Calls[((self._LastCurCall - 1) % 10)] - \
                    self._Last10Calls[self._LastCurCall])

    # Not sure how to implement
    def get_rawtime(self):
        pass

    def get_fps(self):
        avg = 0
        for i in range(0, 10):
            avg += i
        return s2fps(avg / 10)


# Will require cooperation, due to the fact that it is the amount
# of time passed since pygame2.init() was called and it does not
# exist yet.
def get_ticks():
    pass


def wait(ms):
    time.sleep(ms2s(ms))


def delay(ms):
    t1 = time.clock()
    t2 = time.clock()
    while (ms > (t2 - t1)):
        t2 = time.clock()


# We actually need event.py to use this.
def set_timer(eventid, ms):
    pass
