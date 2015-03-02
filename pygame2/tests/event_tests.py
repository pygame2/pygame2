"""
event_tests.py

"""
import unittest
from mock import Mock
from pygame2 import event


class TestDispatcher(event.EventDispatcher):
    def on_test(self):
        pass


class EventDispatcherTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        self.o = TestDispatcher()

    # def test_register_event_type(self):
    # self.o.register_event_type('test')
    #     self.assertIn('test', self.o.events)
    #     self.assertEqual(len(self.o.events), 1)
    #
    # def test_unregister_event_type_ok(self):
    #     self.o.register_event_type('test')
    #     self.o.unregister_event_type('test')
    #     self.assertNotIn('test', self.o.events)
    #     self.assertEqual(len(self.o.events), 0)
    #
    # def test_unregister_event_type_missing(self):
    #     self.o.unregister_event_type('test')
    #
    # def test_bind_self(self):
    #     # self.o.register_event_type('test')
    #     self.o.bind('test')
    #
    # def test_dispatch_no_event(self):
    #     with self.assertRaises(event.NoHandlerException):
    #         self.o.dispatch('test')

    def test_empty_events(self):
        self.assertEqual(len(self.o.events), 0)

    def test_bind_function(self):
        def f():
            pass

        self.o.bind('test', f)

    def test_bind_method(self):
        self.o.bind('test', self.o.on_test)

    def test_bind_and_dispatch_ok(self):
        f = Mock()
        self.o.bind('test', f)
        self.o.dispatch('test')
        self.assertTrue(f.called)

    def test_bind_will_register_new_event_type(self):
        f = Mock()
        self.assertNotIn('test', self.o.events)
        self.assertEqual(len(self.o.events), 0)
        self.o.bind('test', f)
        self.assertIn('test', self.o.events)
        self.assertEqual(len(self.o.events), 1)
