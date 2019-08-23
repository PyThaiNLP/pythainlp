import sys

from . import corpus
from . import tokenization
from . import soundex
from . import tagging

available_namespaces = sorted(['corpus', 'tokenization', 'soundex', 'tagging'])

cli_name = "pythainlp"


def make_usage(s):
    prog = f"{cli_name} {s}"

    return dict(
        prog=prog,
        usage="%(prog)s command [options]"
    )


def exit_if_empty(d, parser):
    if not d:
        parser.print_help()
        sys.exit(0)
