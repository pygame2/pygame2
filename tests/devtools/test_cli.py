
from unittest import TestCase
from mock import Mock
from argparse import ArgumentParser
from pygame2.devtools.cli import CommandLineInterface, Command


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
