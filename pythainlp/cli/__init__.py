import sys

from . import corpus
from . import tokenize
from . import soundex
from . import tag

# namespaces should be verbs (actions) when possible
available_namespaces = sorted(['corpus', 'tokenize', 'soundex', 'tag'])

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
