# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import argparse
import sys
from typing import Optional

from pythainlp import cli


def main(argv: Optional[list[str]] = None) -> None:
    """ThaiNLP command line."""
    if not argv:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog="thainlp",
        description="Thai natural language processing.",
        usage=(
            "thainlp <command> [options]\n\n"
            "Example:\n\n"
            "thainlp data catalog\n\n"
            "--"
        ),
    )
    parser.add_argument(
        "command",
        type=str,
        choices=cli.COMMANDS,
        help="text processing action",
    )

    args = parser.parse_args(argv[1:2])
    cli.exit_if_empty(args.command, parser)

    if hasattr(cli, args.command):
        command = getattr(cli, args.command)
        command.App(argv)


if __name__ == "__main__":
    main(argv=sys.argv)
