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


__all__ = (
    "EventLoop",
    "PlatformEventQueueBase",
    "EventDispatcher",
    "NoHandlerException")

logger = logging.getLogger("pygame2.event")


class EventDispatcher:
    """
    All classes that send or receive events must inherit from this class

    This is not the publish subscribe pattern.  The pub/sub pattern
    dictates that all subscribes will receive messages they are
    subscribed to.  Event dispatchers have a set order in which
    messages are distributed and consumers have the option of
    preventing other consumers from receiving the event.

    TODO:
        implement unschedule (for internal use only?)
        allow consumers to halt propagation of event
        allow arguments to be passed to broadcast (or not)

    names:
        eventually, this psuedo pub/sub will be more like the observer
        pattern, with the queue shoehorned in.  i'd like to keep the names
        'bind and 'dispatch' since they are already in use in popular
        python frameworks and are closer in meaning to the intended function

        event names should follow normal python naming rules
        this will allow for a decorator in the future to decorate
        functions and derive the event name from the function name:

        @window.event
        def on_draw():
            pass

        is the same as, but available in a decorator:
        window.subscribe('on_draw', on_draw)

    concerns:
        how useful is 'setting default arguments when subscribing events'?
    """
    class EventNotRegistered(Exception):
        pass

    class DuplicateEventName(Exception):
        pass

    class NoQueueSetException(Exception):
        pass

    # change to a list or tuple of event names to have them
    # automatically registered when instance is created
    __event_names__ = None

    def __init__(self):
        self._event_types = list()
        self._event_lookup = dict()
        self._subscriptions = list()
        self.queue = None

        event_names = getattr(self, '__events__', None)
        if event_names is not None:
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

        # TODO: verify that event name follows standard python rules

        id = len(self._event_types)
        self._event_types.append(tuple([proxy(a) for a in args]))
        self._event_lookup[event_name] = id
        self._subscriptions.append(list())
        return id

    def get_handled_events(self):
        """Return a list of event names that is handled

        :return: list of event names
        """
        return self._event_lookup.keys()

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

    def subscribe_internal(self, id, callback):
        """Do not use unless you know what you are doing

        Eventually, this will be used internally to provide
        subscribing without slow checks, useful for automation.

        :param id:
        :param callback:
        :return:
        """
        pass

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
