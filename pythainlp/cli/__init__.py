# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""Command line helpers."""
import sys
from argparse import ArgumentParser

from pythainlp.cli import data, soundex, tag, tokenize, benchmark

# a command should start with a verb when possible
COMMANDS = sorted(["data", "soundex", "tag", "tokenize", "benchmark"])

CLI_NAME = "thainlp"


def make_usage(command: str) -> dict:
    prog = f"{CLI_NAME} {command}"

    return {"prog": prog, "usage": f"{prog} [options]"}


def exit_if_empty(command: str, parser: ArgumentParser) -> None:
    if not command:
        parser.print_help()
        sys.exit(0)
