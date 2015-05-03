

def main():
    from argparse import ArgumentParser
    from pygame2.devtools.cli import create_command_line_interface
    parser = ArgumentParser(prog="pygame2")
    cli = create_command_line_interface(parser)
    cli.execute()


if __name__ == "__main__":
    main()
