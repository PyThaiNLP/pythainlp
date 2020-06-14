"""Command line helpers."""
import sys
from argparse import ArgumentParser

from pythainlp.cli import data, soundex, tag, tokenize, benchmark

# a command should be a verb when possible
COMMANDS = sorted(["data", "soundex", "tag", "tokenize", "benchmark"])

CLI_NAME = "thainlp"


def make_usage(command: str) -> dict:
    prog = f"{CLI_NAME} {command}"

    return dict(prog=prog, usage=f"{prog} [options]")


def exit_if_empty(command: str, parser: ArgumentParser) -> None:
    if not command:
        parser.print_help()
        sys.exit(0)
