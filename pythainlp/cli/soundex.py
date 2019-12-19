import argparse

from pythainlp import cli
from pythainlp.soundex import soundex


class App:

    def __init__(self, argv):
        parser = argparse.ArgumentParser("soundex")
        parser.add_argument(
            "-t",
            "--text",
            type=str,
            help="input text",
        )

        parser.add_argument(
            "-e",
            "--engine",
            type=str,
            help="soundex engine [udom83|lk82|metasound] (default: udom83)",
            default="udom83"
        )

        args = parser.parse_args(argv[2:])

        cli.exit_if_empty(args.text, parser)

        sx = soundex(args.text, engine=args.engine)
        print(sx)
