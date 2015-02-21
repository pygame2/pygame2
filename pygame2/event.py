""" pygame2 event functions

this set of functions follows the pygame api

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
"""
import queue
import logging
import pygame2
import weakref


__all__ = (
    "EventType",
    "Event",
    "PlatformEventQueueBase",
    "EventLoop",
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


class EventType:
    """
    An event object
    """

    def __init__(self, event):
        self._event = event

        if not event:
            self.type = None  # NOEVENT
            return

        self.timestamp = event.timestamp
        self.type = event.type

        if self.type in (KEYDOWN, KEYUP):
            # pygame1 definitions
            self.key = event.key.keysym.sym
            self.mod = event.key.keysym.mod
            self.scancode = event.key.keysym.scancode
            self.unicode = None
            self.window_id = event.windowID
            self.repeat = event.repeat

        # pygame2 only
        elif self.type == TEXTEDITING:
            logger.debug("type %s not implemented", self.type)
            return

        # pygame2 only
        elif self.type == TEXTINPUT:
            self.window_id = event.windowID
            self.test = event.text

        elif self.type == MOUSEMOTION:
            self.pos = event.x, event.y
            self.rel = event.xrel, event.yrel
            # TODO: buttons

        elif self.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            self.pos = event.x, event.y
            self.button = event.button
            self.window_id = event.windowID

        elif self.type == MOUSEWHEEL:
            self.window_id = event.windowID
            self.x = event.x
            self.y = event.y

        elif self.type == JOYAXISMOTION:
            self.joy = event.which
            self.axis = event.axis
            # TODO: axis insanity

        elif self.type == JOYBALLMOTION:
            self.joy = event.which
            self.ball = event.ball
            self.rel = event.xrel, event.yrel

        elif self.type == JOYHATMOTION:
            logger.debug("type %s not implemented", self.type)
            return

        elif self.type in (JOYBUTTONDOWN, JOYBUTTONUP):
            self.joy = event.which
            self.button = event.button

        elif self.type == JOYDEVICEADDED:
            self.joy = event.which

        elif self.type == JOYDEVICEREMOVED:
            self.joy = event.which

        # TODO: Controller Events

        elif self.type in (FINGERDOWN, FINGERUP, FINGERMOTION):
            # unlike other event types, coordinates are normalized
            self.touchid = event.touchid
            self.fingerid = event.fingerid
            self.x = event.x
            self.y = event.y
            self.dx = event.dx
            self.dy = event.dy
            self.pressure = event.pressure


def Event(type_id, attr_dict=None, **attrs):
    """
    Event(type, dict) -> EventType instance
    """
    pass


class EventDispatcher:
    """
    All classes that send or receive events must inherit from this class

    event callbacks do not accept positional or keyword arguments

    if you want to pass arguments, use functools.partial
    """

    def register_event_type(self, name):
        """register new event type

        event names must start with 'on_'

        :param name:
        :type name:
        :return:
        :rtype:
        """
        verify_name(name)
        raise NotImplementedError

    def unregister_event_type(self, name):
        """Unregister the event

        :param name:
        :type name:
        :return:
        :rtype:
        """
        raise NotImplementedError

    def dispatch(self, name):
        """Dispatch a single event

        :param name:
        :type name:
        :return:
        :rtype:
        """
        # TODO: check if event_type is valid for this instance
        # if not valid: raise NoHandlerException
        pass

    @property
    def events(self):
        """Return list of all events this object responds to

        :return:
        :rtype: list
        """
        pass

    def bind(self, *args, **kwargs):
        """Bind a callback to an event name

        self.bind(on_key_down=handle_key_down)

        these will do the same:
        self.bind(on_mouse_move=self.on_mouse_move)
        self.bind('on_mouse_move')
        """

        def bind(name, callback):
            verify_name(name)
            assert callable(callback), '{!r} is not callable'.format(callback)
            # TODO: search for a previous handler
            wm = weakref.WeakMethod(callback)
            self.bind_internal(name, wm)

        for name in args:
            callback = getattr(self, name, None)
            if callback is None:
                raise NoHandlerException(
                    'missing handler of event: {}'.format(name))
            bind(name, callback)

        for name, callback in kwargs.items():
            bind(name, callback)

    def bind_internal(self, name, callback):
        """Bind one event.

        To be used internally, by pygame2.
        has basically zero checks on the parameters, so use with caution!
        """
        pass

    def unbind(self, name, callback):
        """ use weakmethods """
        pass


class PlatformEventQueueBase(EventDispatcher):
    """
    To be extended by each host layer
    """
    def __init__(self):
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

    def get_blocked(self, event_types):
        """test if a type of event is blocked from the queue

        get_blocked(type) -> bool

        Returns true if the given event type is blocked from the queue.

        :param event_types:
        :type event_types:
        :return: whether a type of event is blocked from the queue or not
        :rtype: bool
        """
        raise NotImplementedError

    def set_blocked(self, event_types):
        """control which events are allowed on the queue

        set_blocked(type) -> None
        set_blocked(typelist) -> None
        set_blocked(None) -> None

        The given event types are not allowed to appear on the event queue. By
        default all events can be placed on the queue. It is safe to disable an
        event type multiple times.

        If None is raise NotImplementedErrored as the argument, this has the
        opposite effect and ALL of the event types are allowed to be placed
        on the queue.

        :param event_types:
        :type event_types:
        :return: None
        """
        raise NotImplementedError

    def set_allowed(self, event_types):
        """control which events are allowed on the queue

        set_allowed(type) -> None
        set_allowed(typelist) -> None
        set_allowed(None) -> None

        The given event types are allowed to appear on the event queue. By
        default all events can be placed on the queue. It is safe to enable an
        event type multiple times.

        If None is raise NotImplementedErrored as the argument, NONE of the
        event types are allowed to be placed on the queue.

        :param event_types:
        :type event_types:
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
                    timeout = self.clock.get_idle_time()
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
