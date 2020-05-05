"""
thainlp tokenize command line.
"""

import argparse

from pythainlp import cli
from pythainlp.tokenize import (
    DEFAULT_SENT_TOKENIZE_ENGINE,
    DEFAULT_SUBWORD_TOKENIZE_ENGINE,
    DEFAULT_SYLLABLE_TOKENIZE_ENGINE,
    DEFAULT_WORD_TOKENIZE_ENGINE,
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    word_tokenize,
)

DEFAULT_SENT_TOKEN_SEPARATOR = "@@"
DEFAULT_SUBWORD_TOKEN_SEPARATOR = "/"
DEFAULT_SYLLABLE_TOKEN_SEPARATOR = "~"
DEFAULT_WORD_TOKEN_SEPARATOR = "|"


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

        cli.exit_if_empty(args.text, parser)
        result = self.run(
            args.text,
            engine=args.algorithm,
            keep_whitespace=args.keep_whitespace,
        )
        print(args.separator.join(result) + args.separator)


class WordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):
        self.keep_whitespace = True
        self.algorithm = DEFAULT_WORD_TOKENIZE_ENGINE
        self.separator = DEFAULT_WORD_TOKEN_SEPARATOR
        self.run = word_tokenize
        super().__init__(*args, **kwargs)


class SyllableTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):
        self.keep_whitespace = True
        self.algorithm = DEFAULT_SYLLABLE_TOKENIZE_ENGINE
        self.separator = DEFAULT_SYLLABLE_TOKEN_SEPARATOR
        self.run = syllable_tokenize
        super().__init__(*args, **kwargs)


class SentenceTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):
        self.keep_whitespace = True
        self.algorithm = DEFAULT_SENT_TOKENIZE_ENGINE
        self.separator = DEFAULT_SENT_TOKEN_SEPARATOR
        self.run = sent_tokenize
        super().__init__(*args, **kwargs)


class SubwordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):
        self.keep_whitespace = True
        self.algorithm = DEFAULT_SUBWORD_TOKENIZE_ENGINE
        self.separator = DEFAULT_SUBWORD_TOKEN_SEPARATOR
        self.run = subword_tokenize
        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tokenize"))
        parser.add_argument(
            "subcommand", type=str, help="[subword|syllable|word|sent]",
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
            SentenceTokenizationApp("sent", argv)
        else:
            print(f"Subcommand not available: {subcommand}")
