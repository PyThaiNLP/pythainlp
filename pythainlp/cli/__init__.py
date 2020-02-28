import sys

from . import corpus
from . import tokenize
from . import soundex
from . import tag

# commands should be verb when possible
COMMANDS = sorted(['corpus', 'tokenize', 'soundex', 'tag'])

CLI_NAME = "thainlp"


def make_usage(s):
    prog = f"{CLI_NAME} {s}"

    return dict(
        prog=prog,
        usage="%(prog)s command [subcommand] [options]"
    )


def exit_if_empty(d, parser):
    if not d:
        parser.print_help()
        sys.exit(0)
