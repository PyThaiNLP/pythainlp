# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Command line for PyThaiNLP's taggers."""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from pythainlp import cli
from pythainlp.tag import pos_tag
from pythainlp.tools import safe_print

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


class SubAppBase:
    separator: str
    run: Callable[[list[str]], list[tuple[str, str]]]
    args: argparse.Namespace

    def __init__(self, name: str, argv: Sequence[str]) -> None:
        parser = argparse.ArgumentParser(**cli.make_usage("tag " + name))  # type: ignore[arg-type]
        parser.add_argument(
            "text",
            type=str,
            help="input text",
        )
        parser.add_argument(
            "-s",
            "--sep",
            dest="separator",
            type=str,
            help=f"Token separator for input text. default: {self.separator}",
            default=self.separator,
        )

        args = parser.parse_args(argv)
        self.args: argparse.Namespace = args

        tokens = args.text.split(args.separator)
        result = self.run(tokens)

        for word, tag in result:
            safe_print(word + " / " + tag)


class POSTaggingApp(SubAppBase):
    separator: str
    run: Callable[[list[str]], list[tuple[str, str]]]

    def __init__(self, *args: str, **kwargs: str) -> None:
        self.separator: str = "|"
        self.run: Callable[[list[str]], list[tuple[str, str]]] = pos_tag

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv: Sequence[str]) -> None:
        parser = argparse.ArgumentParser(
            prog="tag",
            description="Annotate a text with linguistic information",
            usage=(
                'thainlp tag <tag_type> [--sep "<separator>"] "<text>"\n\n'
                "tag_type:\n\n"
                "pos                part-of-speech\n\n"
                "<separator> and <text> should be inside double quotes.\n"
                "<text> should be a tokenized text, "
                "with tokens separated by <separator>.\n\n"
                "Example:\n\n"
                'thainlp tag pos -s " " "แรงดึงดูด เก็บ หัว คุณ ลง"\n\n'
                "--"
            ),
        )
        parser.add_argument("tag_type", type=str, help="[pos]")

        args = parser.parse_args(argv[2:3])
        cli.exit_if_empty(args.tag_type, parser)
        tag_type = str.lower(args.tag_type)

        argv = argv[3:]

        if tag_type == "pos":
            POSTaggingApp("Part-of-Speech tagging", argv)  # type: ignore[arg-type]
        else:
            print(f"Tag type not available: {tag_type}")
