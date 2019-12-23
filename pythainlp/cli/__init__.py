"""Command line helpers."""
import sys

from . import data, soundex, tag, tokenize

# commands should be verb when possible
COMMANDS = sorted(["data", "soundex", "tag", "tokenize"])

CLI_NAME = "thainlp"


def make_usage(s):
    prog = f"{CLI_NAME} {s}"

    return dict(prog=prog, usage="%(prog)s [options]")


def exit_if_empty(d, parser):
    if not d:
        parser.print_help()
        sys.exit(0)
