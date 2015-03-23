"""
animation tests
"""
from mock import Mock
from pygame2.animation import Animation
from unittest import TestCase


class TestObject:
    """ Mocks don't work well with animations due to introspection,
    so this is to be used instead of a mock.
    """

    def __init__(self):
        self.value = 0.0
        self.illegal_value = 'spam'

    def set_value(self, value):
        self.value = value

    def get_initial(self):
        return .5

    def get_illegal_value(self):
        return self.illegal_value


class AnimationTests(TestCase):
    def setUp(self):
        self.m = TestObject()

    def simulate(self, animation, times=100):
        """ used to simulate a clock updating the animation for some time
        default is one second
        """
        for time in range(times):
            animation.update(.01)

    def test_round_values(self):
        """ verify that values are rounded to the nearest whole integer
        """
        a = Animation(value=1.1, round_values=True)
        a.start(self.m)

        # verify that it rounds down (.25 => 0)
        self.simulate(a, 25)
        self.assertEqual(self.m.value, 0)

        # verify that it rounds up (.75 => 1)
        self.simulate(a, 50)
        self.assertEqual(self.m.value, 1)

        # verify that final value is also rounded
        self.simulate(a, 25)
        self.assertEqual(self.m.value, 1)

    def test_start_will_not_set_values(self):
        """ verify that the animation will not change values at start
        """
        a = Animation(value=1)
        a.start(self.m)
        self.assertEqual(self.m.value, 0)

    def test_target_attribute(self):
        """ verify that the animation can modify normal attributes
        """
        a = Animation(value=1)
        a.start(self.m)
        self.simulate(a)
        self.assertEqual(self.m.value, 1)

    def test_target_callable(self):
        """ verify that the animation will update callable attributes
        """
        a = Animation(set_value=1)
        a.start(self.m)
        self.simulate(a)
        self.assertEqual(self.m.value, 1)

    def test_set_initial(self):
        """ verify that the animation will set initial values
        """
        a = Animation(value=1, initial=.5)
        a.start(self.m)

        # this will set the value to the initial
        a.update(0)
        self.assertEqual(self.m.value, .5)

    def test_set_initial_callable(self):
        """ verify that the animation will set initial values from a callable
        """
        a = Animation(value=1, initial=self.m.get_initial)
        a.start(self.m)

        # this will set the value to the initial
        a.update(0)
        self.assertEqual(self.m.value, .5)

    def test_delay(self):
        """ verify that this will not start until the delay
        """
        a = Animation(value=1, delay=1)
        a.start(self.m)

        self.simulate(a, 100)
        self.assertEqual(self.m.value, 0)

        self.simulate(a, 100)
        self.assertEqual(self.m.value, 1)

    def test_finish_before_complete(self):
        """ verify that calling finish before complete will set final values
        """
        a = Animation(value=1)
        a.start(self.m)
        a.finish()
        self.assertEqual(self.m.value, 1)

    def test_update_callback_called(self):
        """ verify that update_callback is called each update and final
        """
        m = Mock()
        a = Animation(value=1)
        a.bind('on_update', m)
        a.start(self.m)
        self.simulate(a)
        self.assertTrue(m.called)

        # 101 = 100 iterations of update + 1 iteration during the finalizer
        self.assertEqual(m.call_count, 101)

    def test_final_callback_called(self):
        """ verify that callback is called during the finalizer
        """
        m = Mock()
        a = Animation(value=1)
        a.bind('on_finish', m)
        a.start(self.m)
        self.simulate(a)
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

    def test_non_number_target_raises_valueerror(self):
        a = Animation(value=self.m.illegal_value)
        with self.assertRaises(ValueError):
            a.start(self.m)

        a = Animation(value=self.m.get_illegal_value)
        with self.assertRaises(ValueError):
            a.start(self.m)

    def test_non_number_initial_raises_valueerror(self):
        a = Animation(illegal_value=1)
        with self.assertRaises(ValueError):
            a.start(self.m)

        a = Animation(value=1, initial=self.m.get_illegal_value)
        with self.assertRaises(ValueError):
            a.start(self.m)

    def test_no_targets_raises_valueerror(self):
        with self.assertRaises(ValueError):
            Animation()

    def test_finish_before_start_raises_runtimeerror(self):
        a = Animation(value=1)

        with self.assertRaises(RuntimeError):
            a.finish()

    def test_exceed_duration_raises_runtimeerror(self):
        a = Animation(value=1)
        a.start(self.m)

        with self.assertRaises(RuntimeError):
            self.simulate(a, 101)

    def test_finish_then_update_raises_runtimeerror(self):
        a = Animation(value=1)
        a.start(self.m)
        a.finish()

        with self.assertRaises(RuntimeError):
            a.update(1)

    def test_finish_then_start_raises_runtimeerror(self):
        a = Animation(value=1)
        a.start(self.m)
        a.finish()

        with self.assertRaises(RuntimeError):
            a.start(self.m)

    def test_finish_twice_raises_runtimeerror(self):
        a = Animation(value=1)
        a.start(self.m)
        a.finish()

        with self.assertRaises(RuntimeError):
            a.finish()

    def test_start_twice_raises_runtimeerror(self):
        a = Animation(value=1)
        a.start(self.m)

        with self.assertRaises(RuntimeError):
            a.start(self.m)
