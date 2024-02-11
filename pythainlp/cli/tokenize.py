# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Command line for PyThaiNLP's tokenizers.
"""

import argparse

from pythainlp import cli
from pythainlp.tokenize import (
    DEFAULT_SENT_TOKENIZE_ENGINE,
    DEFAULT_SUBWORD_TOKENIZE_ENGINE,
    DEFAULT_WORD_TOKENIZE_ENGINE,
    sent_tokenize,
    subword_tokenize,
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
            "text",
            type=str,
            nargs="?",
            help="input text",
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
        parser = argparse.ArgumentParser(
            prog="tokenize",
            description="Break a text into small units (tokens).",
            usage=(
                'thainlp tokenize <token_type> [options] "<text>"\n\n'
                "token_type:\n\n"
                "subword            subword (may not be a linguistic unit)\n"
                "syllable           syllable\n"
                "word               word\n"
                "sent               sentence\n\n"
                "options:\n\n"
                "--sep or -s <separator>    specify custom separator\n"
                "                           (default is a space)\n"
                "--algo or -a <algorithm>   tokenization algorithm\n"
                "                           (see API doc for more info)\n"
                "--keep-whitespace or -w    keep whitespaces in output\n"
                "                           (default)\n\n"
                "<separator> and <text> should be inside double quotes.\n\n"
                "Example:\n\n"
                'thainlp tokenize word -s "|" "ใต้แสงนีออนเปลี่ยวเหงา"\n\n'
                "--"
            ),
        )
        parser.add_argument(
            "token_type",
            type=str,
            help="[subword|word|sent]",
        )

        args = parser.parse_args(argv[2:3])
        cli.exit_if_empty(args.token_type, parser)
        token_type = str.lower(args.token_type)

        argv = argv[3:]
        if token_type.startswith("w"):
            WordTokenizationApp("word", argv)
        elif token_type.startswith("su"):
            SubwordTokenizationApp("subword", argv)
        elif token_type.startswith("se"):
            SentenceTokenizationApp("sent", argv)
        else:
            print(f"Token type not available: {token_type}")
