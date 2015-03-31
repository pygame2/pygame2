"""
event_tests.py

"""
from collections import deque
from unittest import TestCase, skip
from mock import Mock, call

from pygame2.event import EventDispatcher


class EventDispatcherTestCase(TestCase):

    def setUp(self):
        self.dispatcher = EventDispatcher()

    def test_register_should_require_an_event_name(self):
        with self.assertRaises(TypeError):
            self.dispatcher.register()

    def test_register_returns_an_event_id(self):
        id = self.dispatcher.register("event-name")
        self.assertIsNotNone(id)

    def test_register_returns_unique_event_ids(self):
        id1 = self.dispatcher.register("event-name-one")
        id2 = self.dispatcher.register("event-name-two")
        self.assertNotEqual(id1, id2)

    def test_cannot_register_same_event_name_twice(self):
        self.dispatcher.register("event-name")
        with self.assertRaises(EventDispatcher.DuplicateEventName):
            self.dispatcher.register("event-name")

    def test_cannot_subscribe_to_event_that_does_not_exist(self):
        with self.assertRaises(KeyError):
            self.dispatcher.subscribe_by_name("event-name", None)

    def test_cannot_subscribe_to_event_with_non_existent_id(self):
        with self.assertRaises(IndexError):
            self.dispatcher.subscribe_by_id(123, None)

    def test_can_broadcast_event_by_name(self):
        self.dispatcher.register("event-name")
        callback = Mock()
        self.dispatcher.subscribe_by_name("event-name", callback)
        self.dispatcher.broadcast_by_name("event-name")
        callback.assert_called_once_with("event-name")

    def test_can_broadcast_by_id(self):
        id = self.dispatcher.register("event-name")
        callback = Mock()
        self.dispatcher.subscribe_by_id(id, callback)
        self.dispatcher.broadcast_by_id(id)
        callback.assert_called_once_with("event-name")

    def test_can_associate_references_with_event_type(self):

        class MyFoo:

            def __init__(self):
                self.i_haz = "things"

        inst = MyFoo()
        id = self.dispatcher.register("event-name", inst)

        callback = Mock()
        self.dispatcher.subscribe_by_id(id, callback)
        self.dispatcher.broadcast_by_id(id)

        callback.assert_called_with("event-name", inst)

    def test_can_add_extra_data_to_broadcast(self):
        self.dispatcher.register("event-name")
        callback = Mock()
        self.dispatcher.subscribe_by_name("event-name", callback)
        self.dispatcher.broadcast("event-name", foo="bar", fizz="buzz")
        callback.assert_called_with("event-name", foo="bar", fizz="buzz")

    def test_can_subscribe(self):
        callback = Mock()

        class DefaultArgs:

            def __init__(self):
                self.foo = "foo"
                self.bar = "bar"

        defaults = DefaultArgs()

        self.dispatcher.subscribe("awesome-event", callback, defaults)
        self.dispatcher.broadcast("awesome-event", extra="sauce")
        callback.assert_called_with("awesome-event", defaults, extra="sauce")


class QueuingEventDispatcherTestCase(TestCase):

    def setUp(self):
        self.dispatcher = EventDispatcher()
        self.dispatcher.register("test-event")
        self.callback = Mock()
        self.dispatcher.subscribe("test-event", self.callback)
        self.queue = deque()
        self.dispatcher.set_queue(self.queue)

    def test_when_queue_present_broadcast_should_enqueue_events_instead_of_calling_them(self):
        self.dispatcher.broadcast("test-event")
        self.assertFalse(self.callback.called)
        self.assertEqual(len(self.queue), 1)

    def test_flush_queue(self):
        self.dispatcher.broadcast("test-event")
        self.dispatcher.broadcast("test-event", foo="foo")
        self.dispatcher.broadcast("test-event", bar="bar", whiz=123)
        self.assertFalse(self.callback.called)
        self.assertEqual(len(self.queue), 3)
        self.dispatcher.flush()
        self.assertIn(call("test-event"), self.callback.mock_calls)
        self.assertIn(call("test-event", foo="foo"), self.callback.mock_calls)
        self.assertIn(call("test-event", bar="bar", whiz=123), self.callback.mock_calls)

    def test_flush_with_no_queue_throws_up(self):
        self.dispatcher.set_queue(None)
        with self.assertRaises(EventDispatcher.NoQueueSetException):
            self.dispatcher.flush()

