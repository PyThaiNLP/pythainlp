#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Command line for PyThaiNLP's benchmarking tools."""

from __future__ import annotations

import argparse
import json
import os
from typing import TYPE_CHECKING

from pythainlp import cli
from pythainlp.tools import safe_print

if TYPE_CHECKING:
    from collections.abc import Sequence


def _read_file(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        lines = (r.strip() for r in f.readlines())
    return list(lines)


class App:
    def __init__(self, argv: Sequence[str]) -> None:
        parser = argparse.ArgumentParser(
            prog="benchmark",
            description=(
                "Benchmark for various tasks;\n"
                "currently, we have only for word tokenization."
            ),
            usage=(
                "thainlp benchmark [task] [task-options]\n\n"
                "tasks:\n\n"
                "word-tokenization      benchmark word tokenization\n\n"
                "--"
            ),
        )

        parser.add_argument("task", type=str, help="[word-tokenization]")

        args = parser.parse_args(argv[2:3])
        cli.exit_if_empty(args.task, parser)
        task = str.lower(args.task)

        task_argv = argv[3:]
        if task == "word-tokenization":
            WordTokenizationBenchmark(task, task_argv)


class WordTokenizationBenchmark:
    def __init__(self, name: str, argv: Sequence[str]) -> None:
        parser = argparse.ArgumentParser(**cli.make_usage("benchmark " + name))  # type: ignore[arg-type]

        parser.add_argument(
            "--input-file",
            action="store",
            help="Path to input file to compare against the test file",
        )

        parser.add_argument(
            "--test-file",
            action="store",
            help="Path to test file i.e. ground truth",
        )

        parser.add_argument(
            "--save-details",
            default=False,
            action="store_true",
            help=(
                "Save comparison details to files (eval-XXX.json"
                " and eval-details-XXX.json)"
            ),
        )

        args = parser.parse_args(argv)

        actual = _read_file(args.input_file)
        expected = _read_file(args.test_file)

        if len(actual) != len(expected):
            raise ValueError(
                "Input and test files do not have the same number of samples"
            )

        safe_print(
            "Benchmarking %s against %s with %d samples in total"
            % (args.input_file, args.test_file, len(actual))
        )

        try:
            import yaml

            from pythainlp.benchmarks import word_tokenization
        except ImportError as e:
            raise ImportError(
                "The 'benchmarks' extra dependencies are required for this command."
                " Install them with: pip install pythainlp[benchmarks]"
            ) from e

        df_raw = word_tokenization.benchmark(expected, actual)

        columns = [
            "char_level:tp",
            "char_level:fp",
            "char_level:tn",
            "char_level:fn",
            "word_level:correctly_tokenized_words",
            "word_level:total_words_in_sample",
            "word_level:total_words_in_ref_sample",
        ]

        statistics = {}

        for c in columns:
            statistics[c] = float(df_raw[c].sum())

        statistics["char_level:precision"] = statistics["char_level:tp"] / (
            statistics["char_level:tp"] + statistics["char_level:fp"]
        )

        statistics["char_level:recall"] = statistics["char_level:tp"] / (
            statistics["char_level:tp"] + statistics["char_level:fn"]
        )

        statistics["word_level:precision"] = (
            statistics["word_level:correctly_tokenized_words"]
            / statistics["word_level:total_words_in_sample"]
        )

        statistics["word_level:recall"] = (
            statistics["word_level:correctly_tokenized_words"]
            / statistics["word_level:total_words_in_ref_sample"]
        )

        safe_print("============== Benchmark Result ==============")

        for c in ["tp", "fn", "tn", "fp", "precision", "recall"]:
            c = f"char_level:{c}"
            v = statistics[c]
            safe_print(f"{c:>40s} {v:.4f}")

        for c in [
            "total_words_in_sample",
            "total_words_in_ref_sample",
            "correctly_tokenized_words",
            "precision",
            "recall",
        ]:
            c = f"word_level:{c}"
            v = statistics[c]
            safe_print(f"{c:>40s} {v:.4f}")

        if args.save_details:
            dir_name = os.path.dirname(args.input_file)
            file_name = args.input_file.split("/")[-1].split(".")[0]

            res_path = "%s/eval-%s.yml" % (dir_name, file_name)
            safe_print("Evaluation result is saved to %s" % res_path)

            with open(res_path, "w", encoding="utf-8") as outfile:
                yaml.dump(statistics, outfile, default_flow_style=False)

            res_path = "%s/eval-details-%s.json" % (dir_name, file_name)
            safe_print("Details of comparisons is saved to %s" % res_path)

            with open(res_path, "w", encoding="utf-8") as f:
                samples = []
                for i, r in enumerate(df_raw.to_dict("records")):
                    expected, actual = r["expected"], r["actual"]
                    del r["expected"]
                    del r["actual"]

                    samples.append(
                        {
                            "metrics": r,
                            "expected": expected,
                            "actual": actual,
                            "id": i,
                        }
                    )

                details = {"metrics": statistics, "samples": samples}

                json.dump(details, f, ensure_ascii=False)
