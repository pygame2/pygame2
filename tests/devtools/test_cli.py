from os.path import join

from unittest import TestCase
from mock import Mock, call, patch
from argparse import ArgumentParser
from collections import namedtuple

from pygame2.devtools.cli import CommandLineInterface, Command, InitCommand


class CommandLineInterfaceTestCase(TestCase):

    def setUp(self):
        self.parser = Mock(spec=ArgumentParser)
        self.cli = CommandLineInterface(self.parser)

    def test_when_adding_a_command_it_should_ask_command_to_modify_argument_parser(self):
        parser = self.parser

        class MockCommand(Command):

            def __init__(self):
                self.called = False

            def add_command(self, arg_parser):
                self.called = arg_parser is parser

        mock_command = MockCommand()
        self.cli.add_command(mock_command)
        self.assertTrue(mock_command.called)

    def test_when_execute_is_called_should_ask_command_if_should_execute(self):

        class MockCommand(Command):

            def __init__(self):
                self.called = False

            def should_execute(self, args):
                self.called = args is not None

        mock_command = MockCommand()
        self.cli.add_command(mock_command)
        self.cli.execute()
        self.assertTrue(mock_command.called)

    class MockExecuteCommand(Command):

        def __init__(self):
            self.called = False

        def should_execute(self, args):
            return True

        def execute(self, args):
            self.called = args is not None

    def test_when_shoud_execute_command_is_executed(self):
        mock_command = self.MockExecuteCommand()
        self.cli.add_command(mock_command)
        self.cli.execute()
        self.assertTrue(mock_command.called)

    def test_should_only_execute_one_command_per_invocation(self):
        mock_command1, mock_command2 = self.MockExecuteCommand(), self.MockExecuteCommand()
        self.cli.add_command(mock_command1)
        self.cli.add_command(mock_command2)
        self.cli.execute()
        self.assertTrue(mock_command1.called)
        self.assertFalse(mock_command2.called)


class InitCommandTestCase(TestCase):

    def setUp(self):
        self.command = InitCommand()

    def test_when_added_should_add_init_arg(self):
        parser = Mock(spec=ArgumentParser)
        self.command.add_command(parser)
        expected = call("init", action="store_true", help=InitCommand.INIT_HELP_TEXT)
        parser.add_argument.assert_has_calls(expected)

    def test_when_added_should_add_project_name_arg(self):
        parser = Mock(spec=ArgumentParser)
        self.command.add_command(parser)
        expected = call("project-name",
                        help=InitCommand.PROJECT_NAME_HELP_TEXT)
        parser.add_argument.assert_has_calls(expected)

    def test_when_init_is_true_in_args_should_execute(self):
        args = namedtuple("Args", ["init"])(True)
        self.assertTrue(self.command.should_execute(args))

    def test_when_init_is_false_in_args_should_not_execute(self):
        args = namedtuple("Args", ["init"])(False)
        self.assertFalse(self.command.should_execute(args))

    @patch("pygame2.devtools.cli.touch")        
    @patch("pygame2.devtools.cli.makedirs")
    def test_when_init_is_executed_should_create_project_skeleton_directories(self, mock_makedirs, mock_touch):
        args = namedtuple("Args", ["project_name"])("FooBar")
        self.command.execute(args)
        mock_makedirs.assert_has_calls([
            call(join("FooBar", "foobar")),
            call(join("FooBar", "tests")),
            call(join("FooBar", "assets", "images")),
            call(join("FooBar", "assets", "sounds")),
            call(join("FooBar", "assets", "music")),
            call(join("FooBar", "assets", "data")),
            call(join("FooBar", "assets", "misc"))])

    @patch("pygame2.devtools.cli.touch")
    @patch("pygame2.devtools.cli.makedirs")    
    def test_when_init_is_executed_should_touch_various_files(self, mock_makedirs, mock_touch):
        args = namedtuple("Args", ["project_name"])("FooBar")
        self.command.execute(args)
        mock_touch.assert_has_calls([
            call(join("FooBar", "README.md")),
            call(join("FooBar", "LICENSE")),
            call(join("FooBar", "ATTRIBUTIONS")),
            call(join("FooBar", "requirements.txt")),
            call(join("FooBar", "setup.py")),
            call(join("FooBar", "setup.cfg")),
            call(join("FooBar", "test", "test_foobar.py")),
            call(join("FooBar", "foobar", "__init__.py")),
            call(join("FooBar", "foobar", "__main__.py")),
            call(join("FooBar", "foobar", "cli.py"))
        ])
