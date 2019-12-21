# -*- coding: utf-8 -*-
import argparse
import sys

from pythainlp import cli


def main(args=None):
    """The main routine of PyThaiNLP command line."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        usage="pythainlp command [subcommand] [options]"
    )

    parser.add_argument(
        "command",
        type=str,
        default="",
        nargs="?",
        help="[%s]" % "|".join(cli.COMMANDS)
    )

    args = parser.parse_args(sys.argv[1:2])

    cli.exit_if_empty(args.command, parser)

    if hasattr(cli, args.command):
        command = getattr(cli, args.command)
        command.App(sys.argv)
    else:
        print(f"Command not available: {args.command}\nPlease run with --help for alternatives")



if __name__ == "__main__":
    main()



