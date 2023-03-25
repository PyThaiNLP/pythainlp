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
"""Command line helpers."""
import sys
from argparse import ArgumentParser

from pythainlp.cli import data, soundex, tag, tokenize, benchmark

# a command should be a verb when possible
COMMANDS = sorted(["data", "soundex", "tag", "tokenize", "benchmark"])

CLI_NAME = "thainlp"


def make_usage(command: str) -> dict:
    prog = f"{CLI_NAME} {command}"

    return dict(prog=prog, usage=f"{prog} [options]")


def exit_if_empty(command: str, parser: ArgumentParser) -> None:
    if not command:
        parser.print_help()
        sys.exit(0)
