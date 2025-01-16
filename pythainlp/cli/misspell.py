# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
import random

from pythainlp.tools.misspell import misspell


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            prog="misspell",
            description="Generate misspelled texts from a given file.",
            usage=(
                "thainlp misspell --file <input_file> [--seed <seed>] "
                "[--misspell-ratio <ratio>] [--output <output_file>]\n\n"
                "Example:\n\n"
                "thainlp misspell --file ./some/data.txt --seed=1 "
                "--misspell-ratio 0.05\n\n"
                "--"
            ),
        )
        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Path to the input file",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Random seed for reproducibility",
        )
        parser.add_argument(
            "--misspell-ratio",
            type=float,
            default=0.05,
            help="Ratio of misspells per 100 characters",
        )
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Path to the output file",
        )

        args = parser.parse_args(argv[2:])

        if args.seed is not None:
            random.seed(args.seed)

        with open(args.file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        misspelled_lines = [
            misspell(line, ratio=args.misspell_ratio) for line in lines
        ]

        if args.output is None:
            base, ext = os.path.splitext(args.file)
            args.output = f"{base}-misspelled-r{args.misspell_ratio}-seed{args.seed}{ext}"

        with open(args.output, "w", encoding="utf-8") as f:
            f.writelines(misspelled_lines)
