"""
thainlp soundex command line.

Take input text from command line.
"""
import argparse

from pythainlp import cli
from pythainlp.soundex import DEFAULT_SOUNDEX_ENGINE, soundex


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            prog="soundex",
            description="Convert a text to its sound-based index.",
        )
        parser.add_argument(
            "-a",
            "--algo",
            dest="algorithm",
            type=str,
            choices=["udom83", "lk82", "metasound"],
            help="soundex algorithm",
            default=DEFAULT_SOUNDEX_ENGINE,
        )
        parser.add_argument(
            "text", type=str, help="input text",
        )

        args = parser.parse_args(argv[2:])

        sdx = soundex(args.text, engine=args.algorithm)
        print(sdx)
