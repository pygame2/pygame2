

class CommandLineInterface(object):

    def __init__(self, arg_parser):
        self.arg_parser = arg_parser
        self.commands = list()

    def add_command(self, command):
        self.commands.append(command)
        command.add_command(self.arg_parser)

    def execute(self):
        args = self.arg_parser.parse_args()
        for command in self.commands:
            if command.should_execute(args):
                command.execute(args)
                break
 

class Command(object):

    def add_command(self, arg_parser):
        pass

    
class InitCommand(object):
    pass

