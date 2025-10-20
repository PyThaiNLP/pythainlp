# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Command line helpers."""

import io
import sys
from argparse import ArgumentError, ArgumentParser
from pythainlp.cli import data, tokenize, soundex, tag, benchmark, misspell

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# a command should start with a verb when possible
COMMANDS = sorted(["data", "soundex", "tag", "tokenize", "benchmark", "misspell"])

CLI_NAME = "thainlp"


def make_usage(command: str) -> dict:
    prog = f"{CLI_NAME} {command}"

    return {"prog": prog, "usage": f"{prog} [options]"}


def exit_if_empty(command: str, parser: ArgumentParser) -> None:
    """Print help and exit if command is empty.

    :param command: command from command line
    :type command: str
    :param parser: parser object of the app
    :type parser: ArgumentParser
    """
    if not command:
        if parser:
            parser.print_help()
        raise ArgumentError(None, "No command provided.")

if __name__ == "__main__":
    # Create a simple mapping from command name to the imported module
    COMMAND_MAP = {
        "tokenize": tokenize,
        "soundex": soundex,
        "tag": tag,
        "benchmark": benchmark,
        "misspell": misspell,
        "data": data,
    }

    # Check if a command was provided and if it's one we know
    if len(sys.argv) > 1 and sys.argv[1] in COMMAND_MAP:
        command = sys.argv[1]
        COMMAND_MAP[command].run()
    else:
        if len(sys.argv) < 2:
            print(f"Error: No command provided. Choose one of: {list(COMMAND_MAP.keys())}", file=sys.stderr)
        else:
            print(f"Error: Unknown command '{sys.argv[1]}'", file=sys.stderr)