"""
event_tests.py
"""
from unittest import TestCase, skip
from mock import Mock, call

from pygame2.event import EventDispatcher


class TestDispatcher(EventDispatcher):
    __events__ = ('on_test', )


class EventDispatcherTestCase(TestCase):

    def setUp(self):
        self.dispatcher = TestDispatcher()

    def test_class_attribute_events_are_registered(self):
        callback = Mock()
        self.dispatcher.subscribe('on_test', callback)
        self.dispatcher.broadcast('on_test')
        self.assertTrue(callback.called)

    def test_register_should_require_an_event_name(self):
        with self.assertRaises(TypeError):
            self.dispatcher.register()

    def test_register_returns_an_event_id(self):
        id = self.dispatcher.register("event-name")
        self.assertIsNotNone(id)
        self.assertTrue(str(id).isdigit())

    def test_register_returns_unique_event_ids(self):
        id1 = self.dispatcher.register("event-name-one")
        id2 = self.dispatcher.register("event-name-two")
        self.assertNotEqual(id1, id2)

    def test_cannot_register_same_event_name_twice(self):
        self.dispatcher.register("event-name")
        with self.assertRaises(EventDispatcher.DuplicateEventName):
            self.dispatcher.register("event-name")

    def test_cannot_subscribe_to_event_that_does_not_exist(self):
        with self.assertRaises(EventDispatcher.EventNotRegistered):
            self.dispatcher.subscribe("event-name", None)

    def test_cannot_subscribe_to_event_with_non_existent_id(self):
        with self.assertRaises(EventDispatcher.EventNotRegistered):
            self.dispatcher.subscribe_by_id(123, None)

    def test_can_broadcast_event_by_name(self):
        self.dispatcher.register("event-name")
        callback = Mock()
        self.dispatcher.subscribe("event-name", callback)
        self.dispatcher.broadcast("event-name")
        callback.assert_called_once_with()

    def test_can_broadcast_by_id(self):
        id = self.dispatcher.register("event-name")
        callback = Mock()
        self.dispatcher.subscribe_by_id(id, callback)
        self.dispatcher.broadcast_by_id(id)
        callback.assert_called_once_with()

    def test_can_associate_references_with_event_type(self):

        class MyFoo:

            def __init__(self):
                self.i_haz = "things"

        inst = MyFoo()
        id = self.dispatcher.register("event-name", inst)

        callback = Mock()
        self.dispatcher.subscribe_by_id(id, callback)
        self.dispatcher.broadcast_by_id(id)

        callback.assert_called_once_with(inst)

    def test_can_add_extra_data_to_broadcast(self):
        self.dispatcher.register("event-name")
        callback = Mock()
        self.dispatcher.subscribe("event-name", callback)
        self.dispatcher.broadcast("event-name", foo="bar", fizz="buzz")
        callback.assert_called_with(foo="bar", fizz="buzz")

    @skip('API review')
    def test_can_subscribe_skip(self):
        callback = Mock()

        class DefaultArgs:

            def __init__(self):
                self.foo = "foo"
                self.bar = "bar"

        defaults = DefaultArgs()

        self.dispatcher.subscribe("awesome-event", callback, defaults)
        self.dispatcher.broadcast("awesome-event", extra="sauce")
        callback.assert_called_with(defaults, extra="sauce")

    def test_can_subscribe(self):
        callback = Mock()
        self.dispatcher.register("awesome-event")
        self.dispatcher.subscribe("awesome-event", callback)
        self.dispatcher.broadcast("awesome-event", extra="sauce")
        callback.assert_called_with(extra="sauce")


class QueuingEventDispatcherTestCase(TestCase):

    def setUp(self):
        self.dispatcher = EventDispatcher()
        self.dispatcher.register("test-event")
        self.callback = Mock()
        self.dispatcher.subscribe("test-event", self.callback)
        # self.queue = deque()
        self.dispatcher.enable_queue()

    def test_when_queue_present_broadcast_should_enqueue_events_instead_of_calling_them(self):
        self.dispatcher.broadcast("test-event")
        self.assertFalse(self.callback.called)
        self.assertEqual(len(self.dispatcher.queue), 1)

    def test_flush_queue(self):
        self.dispatcher.broadcast("test-event")
        self.dispatcher.broadcast("test-event", foo="foo")
        self.dispatcher.broadcast("test-event", bar="bar", whiz=123)
        self.assertFalse(self.callback.called)
        self.assertEqual(len(self.dispatcher.queue), 3)
        self.dispatcher.flush()
        self.assertIn(call(), self.callback.mock_calls)
        self.assertIn(call(foo="foo"), self.callback.mock_calls)
        self.assertIn(call(bar="bar", whiz=123), self.callback.mock_calls)

    @skip
    def test_flush_with_no_queue_throws_up(self):
        self.dispatcher.set_queue(None)
        with self.assertRaises(EventDispatcher.NoQueueSetException):
            self.dispatcher.flush()

