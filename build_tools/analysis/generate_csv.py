#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Generate detailed CSV report from type hint analysis

Usage:
    python generate_csv.py [--input INPUT_JSON] [--output-dir OUTPUT_DIR]

Options:
    --input         Input JSON file (default: ./output/type_hint_analysis.json)
    --output-dir    Directory to save CSV files (default: ./output)
"""
import argparse
import csv
import json
from pathlib import Path


def main():
    """Generate CSV files from type hint analysis JSON."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate CSV reports from type hint analysis"
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON file (default: OUTPUT_DIR/type_hint_analysis.json)",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to save CSV files (default: ./output)",
    )
    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).resolve().parent
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = script_dir / output_dir

    # Default input file is in the output directory
    if args.input is None:
        input_file = output_dir / "type_hint_analysis.json"
    else:
        input_file = Path(args.input)
        if not input_file.is_absolute():
            input_file = script_dir / input_file

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the JSON data
    print(f"Loading data from: {input_file}")
    with open(input_file, "r") as f:
        data = json.load(f)

    # Create CSV for functions without type hints
    functions_no_hints_file = output_dir / "functions_no_hints.csv"
    with open(functions_no_hints_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Function Name",
                "Submodule",
                "Scope",
                "Priority",
                "References",
                "Test Suite",
                "Decorators",
                "File",
                "Line",
            ]
        )

        for func in data["functions_no_hints"]:
            parts = func["name"].split(".")
            submodule = (
                parts[1]
                if len(parts) > 2 and parts[0] == "pythainlp"
                else parts[0]
            )
            decorators = ", ".join(func.get("decorators", []))

            writer.writerow(
                [
                    func["name"],
                    submodule,
                    func["scope"],
                    func["priority"],
                    func["references"],
                    func["test_suite"],
                    decorators,
                    func["file"],
                    func["line"],
                ]
            )

    # Create CSV for functions with incomplete type hints
    functions_incomplete_file = output_dir / "functions_incomplete_hints.csv"
    with open(functions_incomplete_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Function Name",
                "Submodule",
                "Scope",
                "Priority",
                "Params Hinted",
                "Has Return",
                "References",
                "Test Suite",
                "Decorators",
                "File",
                "Line",
            ]
        )

        for func in data["functions_incomplete_hints"]:
            parts = func["name"].split(".")
            submodule = (
                parts[1]
                if len(parts) > 2 and parts[0] == "pythainlp"
                else parts[0]
            )
            decorators = ", ".join(func.get("decorators", []))

            writer.writerow(
                [
                    func["name"],
                    submodule,
                    func["scope"],
                    func["priority"],
                    func["params"],
                    func["return"],
                    func["references"],
                    func["test_suite"],
                    decorators,
                    func["file"],
                    func["line"],
                ]
            )

    # Create summary CSV by submodule
    submodule_summary_file = output_dir / "submodule_summary.csv"
    with open(submodule_summary_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Submodule",
                "Total",
                "Complete",
                "Incomplete",
                "None",
                "% Complete",
                "Mypy Errors",
            ]
        )

        for submodule, counts in sorted(data["by_submodule"].items()):
            total = counts["complete"] + counts["incomplete"] + counts["none"]
            pct = (counts["complete"] / total * 100) if total > 0 else 0
            mypy_errors = counts.get("mypy_errors", 0)

            writer.writerow(
                [
                    submodule,
                    total,
                    counts["complete"],
                    counts["incomplete"],
                    counts["none"],
                    f"{pct:.2f}%",
                    mypy_errors,
                ]
            )

    # Create CSV for class variables without type hints
    class_vars_file = output_dir / "class_variables_no_hints.csv"
    with open(class_vars_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Variable Name",
                "Submodule",
                "Parent Class",
                "Scope",
                "File",
                "Line",
            ]
        )

        for var in data.get("class_variables_no_hints", []):
            parts = var["name"].split(".")
            submodule = (
                parts[1]
                if len(parts) > 2 and parts[0] == "pythainlp"
                else parts[0]
            )

            writer.writerow(
                [
                    var["name"],
                    submodule,
                    var["parent_class"],
                    var["scope"],
                    var["file"],
                    var["line"],
                ]
            )

    # Create CSV for instance variables without type hints
    instance_vars_file = output_dir / "instance_variables_no_hints.csv"
    with open(instance_vars_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Variable Name",
                "Submodule",
                "Parent Class",
                "Scope",
                "File",
                "Line",
            ]
        )

        for var in data.get("instance_variables_no_hints", []):
            parts = var["name"].split(".")
            submodule = (
                parts[1]
                if len(parts) > 2 and parts[0] == "pythainlp"
                else parts[0]
            )

            writer.writerow(
                [
                    var["name"],
                    submodule,
                    var["parent_class"],
                    var["scope"],
                    var["file"],
                    var["line"],
                ]
            )

    # Create CSV for module variables without type hints
    module_vars_file = output_dir / "module_variables_no_hints.csv"
    with open(module_vars_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Variable Name",
                "Submodule",
                "Scope",
                "File",
                "Line",
            ]
        )

        for var in data.get("module_variables_no_hints", []):
            parts = var["name"].split(".")
            submodule = (
                parts[1]
                if len(parts) > 2 and parts[0] == "pythainlp"
                else parts[0]
            )

            writer.writerow(
                [
                    var["name"],
                    submodule,
                    var["scope"],
                    var["file"],
                    var["line"],
                ]
            )

    # Create CSV for type aliases
    type_aliases_file = output_dir / "type_aliases.csv"
    with open(type_aliases_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Type Alias Name",
                "Submodule",
                "Scope",
                "File",
                "Line",
            ]
        )

        for alias in data.get("type_aliases", []):
            parts = alias["name"].split(".")
            submodule = (
                parts[1]
                if len(parts) > 2 and parts[0] == "pythainlp"
                else parts[0]
            )

            writer.writerow(
                [
                    alias["name"],
                    submodule,
                    alias["scope"],
                    alias["file"],
                    alias["line"],
                ]
            )

    print("CSV files generated:")
    print(f"  {functions_no_hints_file}")
    print(f"  {functions_incomplete_file}")
    print(f"  {submodule_summary_file}")
    print(f"  {class_vars_file}")
    print(f"  {instance_vars_file}")
    print(f"  {module_vars_file}")
    print(f"  {type_aliases_file}")


if __name__ == "__main__":
    main()
