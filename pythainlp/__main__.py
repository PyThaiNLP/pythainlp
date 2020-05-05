# -*- coding: utf-8 -*-
import argparse
import sys

from pythainlp import cli


def main(args=None):
    """ThaiNLP command line."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        "thainlp", usage="thainlp <command> [options]"
    )

    parser.add_argument(
        "command",
        type=str,
        choices=cli.COMMANDS,
        help="text processing action",
    )

    args = parser.parse_args(sys.argv[1:2])

    cli.exit_if_empty(args.command, parser)

    if hasattr(cli, args.command):
        command = getattr(cli, args.command)
        command.App(sys.argv)
    else:
        print(f"Command not available: {args.command}")
        print("Please run with --help for alternatives")


if __name__ == "__main__":
    main()
