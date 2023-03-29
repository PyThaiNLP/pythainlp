# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import sys

from pythainlp import cli


def main(argv=None):
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
