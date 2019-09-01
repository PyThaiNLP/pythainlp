import argparse

from pythainlp import cli
from pythainlp.soundex import soundex


class App:

    def __init__(self, argv):
        parser = argparse.ArgumentParser("sounddex")
        parser.add_argument(
            "--text",
            type=str,
            help="text",
        )

        parser.add_argument(
            "--engine",
            type=str,
            help="[udom83|lk82|metasound] (default: udom83)",
            default="udom83"
        )

        args = parser.parse_args(argv[2:])

        cli.exit_if_empty(args.text, parser)

        sx = soundex(args.text, engine=args.engine)
        print(sx)
