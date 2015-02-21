from .rect import Rect
from .surface import Surface

# "required" modules
from . import app
from . import clock
from . import core
from . import event
from . import graphics
from . import group
from . import sprite
from . import surface


# TODO: MAKE SURE THIS STUFF ISN'T CALLED A BUNCH OF TIMES
def get_args():
    from argparse import ArgumentParser
    import logging

    parser = ArgumentParser(prog="pygame2", description="pygame2 init")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING", help="Verbosity of logging output")

    args = parser.parse_args()

    # logger = logging.getLogger("pygame2.__init__")
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(name)s:%(filename)s:%(lineno)d:%(levelname)s: %(message)s")

    # get_args()
