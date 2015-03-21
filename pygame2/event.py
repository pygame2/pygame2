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
Event:  basically jsut some data, probably a python dict or named tuple
Event Queue:  FIFO queue of events from pygame2 framework
Event Loop: Manages the Event Queue.  Used by pygame2.app.App
Platform Event Queue:  OS specific.  Collects events from OS.
"""
import queue
import logging
import pygame2


__all__ = (
    "EventLoop",
    "PlatformEventQueueBase",
    "EventDispatcher",
    "NoHandlerException")

logger = logging.getLogger("pygame2.event")


def verify_name(name):
    """Event names must begin with "on_"

    :param name: Name of event
    :type name: str
    :return: None
    :rtype: None
    """
    if not name.startswith('on_'):
        raise ValueError('Event names must begin with "on_"')


class NoHandlerException(Exception):
    pass


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

    Is this what we want?
    """

    def __init__(self):
        self._event_handlers = dict()

    # def register_event_type(self, name):
    # """register new event type
    #
    # :param name:
    #     :type name:
    #     :return:
    #     :rtype:
    #     """
    #     # verify_name(name)
    #     self._event_handlers[name] = list()
    #
    # def unregister_event_type(self, name):
    #     """Unregister the event
    #
    #     No error will be raised if the event type does not exist
    #
    #     :param name:
    #     :type name:
    #     :return:
    #     :rtype:
    #     """
    #     try:
    #         del self._event_handlers[name]
    #     except KeyError:
    #         pass

    def dispatch(self, name):
        """Dispatch a single event

        :param name:
        :type name:
        :return:
        :rtype:
        """
        # TODO: check if event_type is valid for this instance
        # TODO: if not valid raise NoHandlerException
        try:
            observers = self._event_handlers[name]
        except KeyError:
            return

        for handler in observers:
            # handler = other.get(name, None)
            # if handler is None:
            #     raise NoHandlerException
            handler()

    @property
    def events(self):
        """Return list of all events this object responds to

        :return:
        :rtype: list
        """
        return self._event_handlers.keys()

    def bind(self, *args, **kwargs):
        """Bind a callback to an event name
        #
        # self.bind(on_key_down=handle_key_down)
        #
        # these will do the same:
        #     self.bind(on_mouse_move=self.on_mouse_move)
        #     self.bind('on_mouse_move')

        bind('event name', callback)
        """

        # def bind(name, callback):
        #     verify_name(name)
        #     assert callable(callback), '{!r} is not callable'.format(callback)
        #     # TODO: search for a previous handler
        #     wm = weakref.WeakMethod(callback)
        #     self.bind_internal(name, wm)
        #
        # for name in args:
        #     callback = getattr(self, name, None)
        #     if callback is None:
        #         raise NoHandlerException(
        #             'missing handler of event: {}'.format(name))
        #     bind(name, callback)
        #
        # for name, callback in kwargs.items():
        #     bind(name, callback)

        # TODO: finalize our API
        name, callback = args
        self.bind_internal(name, callback)

    def bind_internal(self, name, callback):
        """Bind one event.

        To be used internally by pygame2.
        has basically zero checks on the parameters,
        so use with caution!
        """
        try:
            observers = self._event_handlers[name]
        except KeyError:
            observers = list()
            self._event_handlers[name] = observers
        observers.append(callback)

    def unbind(self, name, callback):
        """ use weakmethods """
        pass


class PlatformEventQueueBase(EventDispatcher):
    """
    To be extended by each host layer
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

    def get(self, event_filter=None):
        """Get events from the queue
        """
        raise NotImplementedError

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

    def wait(self):
        """wait for a single event from the queue

        wait() -> EventType instance

        Returns a single event from the queue. If the queue is empty this
        function will wait until one is created. The event is removed from the
        queue once it has been returned. While the program is waiting it will
        sleep in an idle state. This is important for programs that want to
        share the system with other applications.

        This can only be called from the thread that has set the video mode.

        :return: event
        :rtype: EventType
        """
        raise NotImplementedError

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

    def stop(self):
        """Stop platform dependant event queue
        """
        raise NotImplementedError


class EventLoop(EventDispatcher):
    """ the lovechild python's asyncio and pyglet's event loop
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
