""" pygame2 event functions

this set of functions roughly follows the pygame api

there is probably excessive abstraction of roles in the module,
considering we are going to push the use of pygame2.app.App,
which does all this magic for the user.

the general idea that pygame2 should be useful to use, and useful
to teach with demands a lot of reusable abstractions.

here is a sample pygame2 newbie:
* wants to 'see' events from the queue and directly manage them
* wants to directly control when and where things are on the screen
* wants to directly call functions on sprites/sprite-objects
* probably wants to use a vanilla list or set to mange sprites
* doesn't want 'game engine magic'

here is a sample pygame2 veteran:
* lets pygame2.app.App do all of the boring work
* uses decorator and event framework
* organizes things into batches/groups
* lets 'game engine magic' do heavy lifting

As an aside, the pygame2 veteran will also want to do some things
a newbie would want, such as directly controlling the event queue,
so by catering to both groups, the library is more usable.

Terms:
Event:  basically just some data, probably a python dict or named tuple
Event Queue:  FIFO queue of events from pygame2 framework
Event Loop: Manages the Event Queue.  Used by pygame2.app.App
Platform Event Queue:  OS specific.  Collects events from OS.
"""
from weakref import proxy
from abc import ABCMeta, abstractmethod
import queue
import logging
from collections import deque

import pygame2


__all__ = (
    "EventLoop",
    "PlatformEventQueueBase",
    "EventDispatcher",
    "NoHandlerException")

logger = logging.getLogger("pygame2.event")


class EventDispatcher:
    """
    All classes that send or receive events must inherit from this class
    event callbacks do not accept positional or keyword arguments
    if you want to pass arguments, use functools.partial

    This is not the publish subscribe pattern.  The pub/sub pattern
    dictates that all subscribes will receive messages they are
    subscribed to.  Event dispatchers have a set order in which
    messages are distributed and consumers have the option of
    preventing other consumers from receiving the event.

    API Hints:
        foo.subscribe('on_bar', foo.on_bar)
        bar.broadcast('on_bar')
        bar.broadcast('on_bar', False)
        bar.broadcast('on_bar', is_it_foobar=True)

    TODO:
       do we require event names to be registered first?
       do we provide a list of event names to handle (related to #1)
       how are errors handled?
       implement unbind and unbind_internal

    names:
        eventually, this psuedo pub/sub will be more like the observer
        pattern, with the queue shoehorned in.  i'd like to keep the names
        'bind and 'dispatch' since they are already in use in popular
        python frameworks and are closer in meaning to the intended function
        (when you disregard the current state of it)

    concerns:
        why are event names being sent back to the subscribers?
        let's simplify sub/broad to 'slow+safe or fast+unsafe' instead of 3 choices (9 combinations!)
        how useful is 'setting default arguments when subscribing events'?
        implement weakref into subscriptions, as we don't want stale refs
    """
    class EventNotRegistered(Exception):
        pass

    class DuplicateEventName(Exception):
        pass

    class NoQueueSetException(Exception):
        pass

    def __init__(self):
        self._event_types = list()
        self._event_lookup = dict()
        self._subscriptions = list()
        self.queue = None

        event_names = getattr(self, '__events__', list())
        for event_name in event_names:
            self.register(event_name)

    def enable_queue(self, queue=None):
        if queue is None:
            self.queue = deque()
        else:
            self.queue = queue

    def register(self, event_name, *args):
        """Register an event name for use

        :param event_name:
        :param args:
        :return:
        """
        if event_name in self._event_lookup:
            raise self.DuplicateEventName()

        id = len(self._event_types)
        self._event_types.append(tuple([proxy(a) for a in args]))
        self._event_lookup[event_name] = id
        self._subscriptions.append(list())
        return id

    def subscribe(self, event_name, callback):
        """Safer and more convenient

        :param event_name:
        :param callback:
        :return: id of subscribed event
        """
        try:
            id = self._event_lookup[event_name]
        except KeyError:
            raise self.EventNotRegistered(self, event_name)
        else:
            self.subscribe_by_id(id, callback)
            return id

    def subscribe_by_id(self, event_id, callback):
        """Safe and fast

        :param event_id:
        :param callback:
        :return: None
        """
        try:
            self._subscriptions[event_id].append(callback)
        except IndexError:
            raise self.EventNotRegistered(self, event_id)

    # def subscribe_internal(self, id, callback):
    #     """Do not use unless you know what you are doing
    #
    #     :param id:
    #     :param callback:
    #     :return:
    #     """
    #     pass

    def broadcast(self, event_name, **kwargs):
        """Least performant, most convenient, flexible

        :param event_name:
        :param kwargs:
        :return:
        """
        try:
            id = self._event_lookup[event_name]
        except KeyError:
            raise self.EventNotRegistered(self, event_name)
        else:
            self.broadcast_by_id(id, **kwargs)

    def broadcast_by_id(self, id, **kwargs):
        """Best performance, least convenient

        :param id:
        :param kwargs:
        :return:
        """
        if self.queue is None:
            self.broadcast_internal(id, **kwargs)
        else:
            self.queue.append((id, kwargs))

    def broadcast_internal(self, event_id, **kwargs):
        """Do not use this directly unless you are absolutely sure you need to

        :param event_id:
        :param kwargs:
        :return:
        """
        try:
            subscriptions = self._subscriptions[event_id]
        except IndexError:
            raise self.EventNotRegistered(self, event_id)
        else:
            event_type = self._event_types[event_id]
            for subscriber in subscriptions:
                subscriber(*event_type, **kwargs)

    def flush(self):
        """Empty out any queued events
        """
        if self.queue is None:
            raise self.NoQueueSetException()

        while len(self.queue) > 0:
            id, kwargs = self.queue.popleft()
            if kwargs is None:
                self.broadcast_internal(id)
            else:
                self.broadcast_internal(id, **kwargs)


class PlatformEventQueueBase(EventDispatcher, metaclass=ABCMeta):
    """
    To be extended by each host layer

    This could also be the monolithic queue for platform and user events

    MODELED AFTER PYGAME
    """

    def __init__(self):
        super().__init__()
        self.event_queue = None

    def start(self):
        """ Start the event loop.  Required for all platforms.

        Must be called before the event loop is run or ticked

        :return: None
        """
        self.event_queue = queue.Queue()
        # TODO: clear out events already in the platform queue

    @abstractmethod
    def get(self, event_filter=None):
        """Get events from the queue
        """
        raise NotImplementedError

    @abstractmethod
    def poll(self):
        """get a single event from the queue

        poll() -> EventType instance

        Returns a single event from the queue. If the event queue is empty an
        event of type pygame.NOEVENT will be returned immediately. The returned
        event is removed from the queue.

        :return: event
        :rtype: EventType
        """
        raise NotImplementedError

    # This feature requires some thought to be implemented correctly
    #
    # def wait(self):
    #     """wait for a single event from the queue
    #
    #     wait() -> EventType instance
    #
    #     Returns a single event from the queue. If the queue is empty this
    #     function will wait until one is created. The event is removed from the
    #     queue once it has been returned. While the program is waiting it will
    #     sleep in an idle state. This is important for programs that want to
    #     share the system with other applications.
    #
    #     This can only be called from the thread that has set the video mode.
    #
    #     :return: event
    #     :rtype: EventType
    #     """
    #     raise NotImplementedError

    @abstractmethod
    def peek(self, types=None):
        """test if event types are waiting on the queue

        peek(type) -> bool
        peek(typelist) -> bool

        Returns true if there are any events of the given type waiting on the
        queue. If a sequence of event types is passed, this will return True if
        any of those events are on the queue.

        :param types:
        :type types:
        :return: bool if event types are waiting on the queue
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def post(self, event):
        """place a new event on the queue

        post(Event) -> bool

        This places a new event at the end of the event queue. These Events will
        later be retrieved from the other queue functions.

        This is usually used for placing pygame.USEREVENT events on the queue.
        Although any type of event can be placed, if using the system event
        types
        your program should be sure to create the standard attributes with
        appropriate values.

        pygame1 note: pygame1 returns None, pygame2 will return a boolean

        :param event:
        :type event or list:
        :return: True on success, False if the event was filtered
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self, event_filter=None):
        """remove all events from the queue

        clear() -> None
        clear(type) -> None
        clear(typelist) -> None

        Remove all events or events of a specific type from the queue. This has
        the same effect as pygame.event.get() except nothing is returned. This
        can be slightly more efficient when clearing a full event queue.

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop platform dependant event queue
        """
        raise NotImplementedError


class EventLoop(EventDispatcher):
    """ the lovechild python's asyncio and pyglet's event loop

    eventually will be integrated into pygame2.app.App

    NOT CURRENTLY IN USE
    """

    def __init__(self):
        super().__init__()
        self.clock = None
        self.platform_queue = None

    def run_forever(self):
        self.clock = pygame2.clock.Clock()

        # check if already running
        # raise runtimeerror if already running
        try:
            while 1:
                try:
                    self.step()
                    # timeout = self.clock.get_idle_time()
                    # self.platform_queue.sleep(timeout)

                except:
                    # this exception should be stoperror or something
                    # meaning the loop is done
                    break
        finally:
            # cleanup
            pass

    def step(self):
        """Do one iteration of event loop

        * lets OS sleep app until next scheduled event
        :return:
        :rtype:
        """
        self.clock.tick()

    def stop(self):
        """stop the event loop
        """
        raise NotImplementedError

    def enter_blocking(self):
        """Called by pyglet internal processes when the operating system
        is about to block due to a user interaction.  For example, this
        is common when the user begins resizing or moving a window.

        This method provides the event loop with an opportunity to set up
        an OS timer on the platform event loop, which will continue to
        be invoked during the blocking operation.

        In a blocked state, the app will hang while waiting for events.
        Setting an OS timer with a callback will allow the app to continue
        to process events, although timing will be different, so it might
        be wise to pause the gameplay during this 'inside blocking' state.

        The default implementation ensures that `idle` continues to be called
        as documented.
        """
        # timeout = self.idle()
        # app.platform_event_loop.set_timer(self._blocking_timer, timeout)
        raise NotImplementedError

    def exit_blocking(self):
        # app.platform_event_loop.set_timer(None, None)
        raise NotImplementedError

    def _blocking_timer(self):
        # timeout = self.idle()
        # app.platform_event_loop.set_timer(self._blocking_timer, timeout)
        raise NotImplementedError
