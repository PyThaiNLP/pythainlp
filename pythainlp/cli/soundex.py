import argparse

from pythainlp import cli
from pythainlp.soundex import soundex


class App:

    def __init__(self, argv):
        parser = argparse.ArgumentParser("soundex")

        parser.add_argument(
            "subcommand",
            type=str,
            nargs="?",
            help="[udom83|lk82|metasound]"
        )

        parser.add_argument(
            "-t",
            "--text",
            type=str,
            help="input text",
        )

        args = parser.parse_args(argv[2:3])

        cli.exit_if_empty(args.subcommand, parser)
        subcommand = str.lower(args.subcommand)

        cli.exit_if_empty(args.text, parser)

        sdx = ""
        if subcommand.startswith("udom"):
            sdx = soundex(args.text, engine="udom83")
        elif subcommand.startswith("lk"):
            sdx = soundex(args.text, engine="lk82")
        elif subcommand.startswith("meta"):
            sdx = soundex(args.text, engine="metasound")
        else:
            raise NotImplementedError(
                f"Subcommand not available: {subcommand}")

        print(sdx)
