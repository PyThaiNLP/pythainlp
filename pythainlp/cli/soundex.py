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
"""
thainlp soundex command line.

Take input text from command line.
"""
import argparse

from pythainlp import cli
from pythainlp.soundex import DEFAULT_SOUNDEX_ENGINE, soundex


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            prog="soundex",
            description="Convert a text to its sound-based index.",
            usage=(
                "thainlp soundex [-a algorithm] <text>\n\n"
                "algorithms:\n\n"
                "udom83\n"
                "lk82\n"
                "metasound\n\n"
                f"Default soundex algorithm is {DEFAULT_SOUNDEX_ENGINE}.\n\n"
                "<text> should be inside double quotes.\n\n"
                "Example:\n\n"
                'thainlp soundex -a lk82 "มอเตอร์ไซค์"\n\n'
                "--"
            ),
        )
        parser.add_argument(
            "-a",
            "--algo",
            dest="algorithm",
            type=str,
            choices=["udom83", "lk82", "metasound"],
            help="soundex algorithm",
            default=DEFAULT_SOUNDEX_ENGINE,
        )
        parser.add_argument(
            "text",
            type=str,
            help="input text",
        )

        args = parser.parse_args(argv[2:])

        sdx = soundex(args.text, engine=args.algorithm)
        print(sdx)
