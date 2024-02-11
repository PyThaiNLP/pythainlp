# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Command line for PyThaiNLP's soundex.

It takes input text from the command line.
"""
import argparse

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
