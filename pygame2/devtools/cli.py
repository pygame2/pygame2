
from os import makedirs, utime
from os.path import join, exists


def touch(fname):
    if exists(fname):
        utime(fname, None)
    else:
        open(fname, 'a').close()


def create_command_line_interface(arg_parser):
    cli = CommandLineInterface(arg_parser)
    cli.add_command(InitCommand())
    return cli


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

    def add_command(self, arg_parser):  # pragma: no cover
        pass

    def execute(self, args):  # pragma: no cover
        pass

    def should_execute(self, args):  # pragma: no cover
        pass

    
class InitCommand(Command):

    INIT_HELP_TEXT = "Create a new pygame2 game skeleton project."
    PROJECT_NAME_HELP_TEXT = "The name of your new project. It should use Pascal case. ex. RemoteLawnmowerUltra."

    DIRS = [("{{PROJECT_NAME}}", "{{project_name}}"),
            ("{{PROJECT_NAME}}", "tests"),
            ("{{PROJECT_NAME}}", "assets", "images"),
            ("{{PROJECT_NAME}}", "assets", "sounds"),
            ("{{PROJECT_NAME}}", "assets", "music"),
            ("{{PROJECT_NAME}}", "assets", "data"),
            ("{{PROJECT_NAME}}", "assets", "misc")]

    FILES = [("{{PROJECT_NAME}}", "README.md"),
             ("{{PROJECT_NAME}}", "LICENSE"),
             ("{{PROJECT_NAME}}", "ATTRIBUTIONS"),
             ("{{PROJECT_NAME}}", "requirements.txt"),
             ("{{PROJECT_NAME}}", "setup.py"),
             ("{{PROJECT_NAME}}", "setup.cfg"),
             ("{{PROJECT_NAME}}", "tests", "test_{{project_name}}.py"),
             ("{{PROJECT_NAME}}", "{{project_name}}", "__init__.py"),
             ("{{PROJECT_NAME}}", "{{project_name}}", "__main__.py"),
             ("{{PROJECT_NAME}}", "{{project_name}}", "cli.py") ]
    
    def add_command(self, arg_parser):
        subparsers = arg_parser.add_subparsers(help="init", dest="init")
        subparser = subparsers.add_parser("init", help=self.INIT_HELP_TEXT)
        subparser.add_argument("project_name", help=self.PROJECT_NAME_HELP_TEXT)
    
    def should_execute(self, args):
        return args.init

    def execute(self, args):
        self.create_directories(args)
        self.create_files(args)

    def create_directories(self, args):
        for d in self.DIRS:
            templated = self.replace_tokens(d, args)
            makedirs(join(*templated))

    def create_files(self, args):
        for f in self.FILES:
            templated = self.replace_tokens(f, args)
            touch(join(*templated))

    def replace_tokens(self, segments, args):
        output = list()
        for s in segments:
            s = s.replace("{{PROJECT_NAME}}", args.project_name)
            s = s.replace("{{project_name}}", args.project_name.lower())
            output.append(s)
        return tuple(output)
