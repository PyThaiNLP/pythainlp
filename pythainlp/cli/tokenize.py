"""
thainlp tokenize command line.
"""
import argparse

from pythainlp import cli
from pythainlp.tokenize import (
    word_tokenize,
    subword_tokenize,
    syllable_tokenize,
    sent_tokenize,
)


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tokenize " + name))
        parser.add_argument(
            "text", type=str, nargs="?", help="input text",
        )
        parser.add_argument(
            "-s",
            "--sep",
            dest="separator",
            type=str,
            help=f"default: {self.separator}",
            default=self.separator,
        )
        parser.add_argument(
            "-a",
            "--algo",
            dest="algorithm",
            type=str,
            help=f"default: {self.algorithm}",
            default=self.algorithm,
        )
        parser.add_argument(
            "-w",
            "--keep-whitespace",
            dest="keep_whitespace",
            action="store_true",
        )
        parser.add_argument(
            "-nw",
            "--no-whitespace",
            dest="keep_whitespace",
            action="store_false",
        )
        parser.set_defaults(keep_whitespace=True)

        args = parser.parse_args(argv)

        self.args = args
        print(args)

        cli.exit_if_empty(args.text, parser)

        result = self.run(
            args.text, engine=args.algorithm, keep_whitespace=args.keep_whitespace
        )
        print(args.separator.join(result) + args.separator)


class WordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algorithm = "newmm"
        self.separator = "|"
        self.run = word_tokenize

        super().__init__(*args, **kwargs)


class SyllableTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algorithm = "ssg"
        self.separator = "~"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class SentenceTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algorithm = "crfcut"
        self.separator = "^"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class SubwordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algorithm = "tcc"
        self.separator = "/"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tokenize"))
        parser.add_argument(
            "subcommand",
            type=str,
            help="[subword|syllable|word|sent]",
        )

        args = parser.parse_args(argv[2:3])

        cli.exit_if_empty(args.subcommand, parser)
        subcommand = str.lower(args.subcommand)

        argv = argv[3:]

        if subcommand.startswith("w"):
            WordTokenizationApp("word", argv)
        elif subcommand.startswith("sy"):
            SyllableTokenizationApp("syllable", argv)
        elif subcommand.startswith("su"):
            SubwordTokenizationApp("subword", argv)
        elif subcommand.startswith("se"):
            SubwordTokenizationApp("sent", argv)
        else:
            print(f"Subcommand not available: {subcommand}")
