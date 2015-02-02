"""
event_tests.py

"""

# from unittest import TestCase
# from logging import getLogger

# import pygame2.event

# logger = getLogger()


# class EventTests(TestCase):

# def setUp(self):
# pygame2.display.init()
#         pygame2.event.clear()
#         self.assertFalse(pygame2.event.get())

#         self.test_type = pygame2.event.KEYDOWN
#         self.test_types = [pygame2.event.KEYDOWN, pygame2.event.KEYUP]

#     def test_pump(self):
#         """
#         just check that it won't raise any errors
#         """
#         self.assertIsNone(pygame2.event.pump())

#     def test_get(self):
#         for i in range(20):
#             event = pygame2.event.Event(self.test_type)
#             pygame2.event.post(event)
#         self.assertGreaterEqual(len(pygame2.event.get()), 20)

#     def test_poll(self):
#         self.assertIsInstance(pygame2.event.poll(), pygame2.event.EventType)

#     def test_wait(self):
#         event = pygame2.event.Event(self.test_type)
#         pygame2.event.post(event)
#         self.assertIsInstance(pygame2.event.poll(), pygame2.event.EventType)

#     def test_peek_type(self):
#         event = pygame2.event.Event(self.test_type)
#         pygame2.event.post(event)
#         self.assertTrue(pygame2.event.peek(self.test_type))

#     def test_peek_typelist(self):
#         for test_type in self.test_types:
#             event = pygame2.event.Event(test_type)
#             pygame2.event.post(event)
#         self.assertTrue(pygame2.event.peek(self.test_types))

#     def test_clear(self):
#         for i in range(20):
#             event = pygame2.event.Event()
#             pygame2.event.post(event)
#         self.assertIsNot(pygame2.event.poll(), pygame2.event.NOEVENT)
#         pygame2.event.clear()
#         self.assertIs(pygame2.event.poll(), pygame2.event.NOEVENT)

#     def test_event_name(self):
#         self.fail()

#     def test_get_blocked(self):
#         pygame2.event.set_blocked(self.test_type)
#         self.assertTrue(pygame2.event.get_blocked(self.test_type))

#     def test_set_blocked_type(self):
#         pygame2.event.set_blocked(self.test_type)
#         self.assertTrue(pygame2.event.get_blocked(self.test_type))

#         # inject an event to make sure it is truly blocked
#         event = pygame2.event.Event(self.test_type)
#         pygame2.event.post(event)

#         events = pygame2.event.get()
#         blocked = [e for e in events if e.type == self.test_type]
#         self.assertListEqual(blocked, [])

#     def test_set_blocked_list(self):
#         pygame2.event.set_blocked(self.test_types)

#         # test the types in the block list
#         for test_type in self.test_types:
#             self.assertTrue(pygame2.event.get_blocked(test_type))

#             # inject some events to test in next step
#             event = pygame2.event.Event(test_type)
#             pygame2.event.post(event)

#         events = pygame2.event.get()
#         blocked = [e for e in events if e.type in self.test_types]
#         self.assertListEqual(blocked, [])

#     def test_set_blocked_none(self):
#         pygame2.event.set_blocked(self.test_type)
#         pygame2.event.set_blocked(None)
#         self.assertFalse(pygame2.event.get_blocked(self.test_type))
#         # TODO: iterate over all know event types an verify they are not
# blocked

#     def test_set_allowed_type(self):
#         pygame2.event.set_allowed(self.test_type)

#         # inject event to verify that it is allowed
#         event = pygame2.event.Event(self.test_type)
#         pygame2.event.post(event)

#         events = pygame2.event.get()
#         allowed = [e for e in events if e.type == self.test_type]
#         self.assertGreater(len(allowed), 0)

#     def test_set_allowed_typelist(self):
#         pygame2.event.set_allowed(self.test_types)
#         for self.test_type in self.test_types:
#             event = pygame2.event.Event(self.test_type)
#             pygame2.event.post(event)

#         events = pygame2.event.get()
#         allowed = [e for e in events if e.type in self.test_types]
#         self.assertGreater(len(allowed), 0)

#     def test_set_allowed_none(self):
#         pygame2.event.set_allowed(None)
#         event = pygame2.event.Event(self.test_type)
#         pygame2.event.post(event)
#         events = pygame2.event.get()
#         self.assertListEqual(events, [])

#     def test_grab(self):
#         pygame2.event.set_grab(True)
#         self.assertTrue(pygame2.event.get_grab())
#         pygame2.event.set_grab(False)
#         self.assertFalse(pygame2.event.get_grab())

#     def test_post(self):
#         event = pygame2.event.Event(self.test_type)
#         pygame2.event.post(event)
#         new_event = pygame2.event.get()
#         self.assertEquals(new_event, event)

#     def test_event_equality(self):
#         a = pygame2.event.Event(1, a=1)
#         b = pygame2.event.Event(1, a=1)
#         c = pygame2.event.Event(2, a=1)
#         d = pygame2.event.Event(1, a=2)

#         self.failUnless(a == a)
#         self.failIf(a != a)
#         self.failUnless(a == b)
#         self.failIf(a != b)
#         self.failUnless(a !=  c)
#         self.failIf(a == c)
#         self.failUnless(a != d)
#         self.failIf(a == d)
