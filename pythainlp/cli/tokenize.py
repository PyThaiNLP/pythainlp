# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Command line for PyThaiNLP's tokenizers."""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING, Any

from pythainlp import cli
from pythainlp.tokenize import (
    DEFAULT_SENT_TOKENIZE_ENGINE,
    DEFAULT_SUBWORD_TOKENIZE_ENGINE,
    DEFAULT_WORD_TOKENIZE_ENGINE,
    sent_tokenize,
    subword_tokenize,
    word_tokenize,
)
from pythainlp.tools import safe_print

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

DEFAULT_SENT_TOKEN_SEPARATOR: str = "@@"  # noqa: S105
DEFAULT_SUBWORD_TOKEN_SEPARATOR: str = "/"  # noqa: S105
DEFAULT_SYLLABLE_TOKEN_SEPARATOR: str = "~"  # noqa: S105
DEFAULT_WORD_TOKEN_SEPARATOR: str = "|"  # noqa: S105


class SubAppBase:
    separator: str
    algorithm: str
    run: Callable[..., Any]
    keep_whitespace: bool
    args: argparse.Namespace

    def __init__(self, name: str, argv: Sequence[str]) -> None:
        parser = argparse.ArgumentParser(**cli.make_usage("tokenize " + name))  # type: ignore[arg-type]
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
        self.args: argparse.Namespace = args

        cli.exit_if_empty(args.text, parser)
        result = self.run(
            args.text,
            engine=args.algorithm,
            keep_whitespace=args.keep_whitespace,
        )
        safe_print(args.separator.join(result) + args.separator)


class WordTokenizationApp(SubAppBase):
    def __init__(self, *args: str, **kwargs: str) -> None:
        self.keep_whitespace: bool = True
        self.algorithm: str = DEFAULT_WORD_TOKENIZE_ENGINE
        self.separator: str = DEFAULT_WORD_TOKEN_SEPARATOR
        self.run: Callable[..., Any] = word_tokenize
        super().__init__(*args, **kwargs)


class SentenceTokenizationApp(SubAppBase):
    def __init__(self, *args: str, **kwargs: str) -> None:
        self.keep_whitespace: bool = True
        self.algorithm: str = DEFAULT_SENT_TOKENIZE_ENGINE
        self.separator: str = DEFAULT_SENT_TOKEN_SEPARATOR
        self.run: Callable[..., Any] = sent_tokenize
        super().__init__(*args, **kwargs)


class SubwordTokenizationApp(SubAppBase):
    def __init__(self, *args: str, **kwargs: str) -> None:
        self.keep_whitespace: bool = True
        self.algorithm: str = DEFAULT_SUBWORD_TOKENIZE_ENGINE
        self.separator: str = DEFAULT_SUBWORD_TOKEN_SEPARATOR
        self.run: Callable[..., Any] = subword_tokenize
        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv: Sequence[str]) -> None:
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
            WordTokenizationApp("word", argv)  # type: ignore[arg-type]
        elif token_type.startswith("su"):
            SubwordTokenizationApp("subword", argv)  # type: ignore[arg-type]
        elif token_type.startswith("se"):
            SentenceTokenizationApp("sent", argv)  # type: ignore[arg-type]
        else:
            safe_print(f"Token type not available: {token_type}")
