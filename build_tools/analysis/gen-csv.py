#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Generate detailed CSV report from type annotation analysis.

Usage:
    python gen-csv.py [--input INPUT_JSON] [--output-dir OUTPUT_DIR]

Options:
    --input         Input JSON file (default: ./output/type_hint_analysis.json)
    --output-dir    Directory to save CSV files (default: ./output)
"""

import argparse
import csv
import json
from pathlib import Path


def _submodule_of(name: str) -> str:
    """Return the submodule of a dotted name, such as "tokenize"."""
    parts = name.split(".")
    if len(parts) > 2 and parts[0] == "pythainlp":
        return parts[1]
    return parts[0]


def _resolve_paths(
    input_arg: str | None, output_arg: str
) -> tuple[Path, Path]:
    """
    Return the input JSON file and the output directory as paths.

    A relative path is resolved against the script directory.
    """
    script_dir = Path(__file__).resolve().parent
    output_dir = Path(output_arg)
    if not output_dir.is_absolute():
        output_dir = script_dir / output_dir

    # Default input file is in the output directory
    if input_arg is None:
        return output_dir / "type_hint_analysis.json", output_dir

    input_file = Path(input_arg)
    if not input_file.is_absolute():
        input_file = script_dir / input_file
    return input_file, output_dir


def main():
    """Generate CSV files from type annotation analysis JSON."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate CSV reports from type annotation analysis"
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

    input_file, output_dir = _resolve_paths(args.input, args.output_dir)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the JSON data
    print(f"Loading data from: {input_file}")
    with open(input_file) as f:
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
            submodule = _submodule_of(func["name"])
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
            submodule = _submodule_of(func["name"])
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
            submodule = _submodule_of(var["name"])

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
            submodule = _submodule_of(var["name"])

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
            submodule = _submodule_of(var["name"])

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
            submodule = _submodule_of(alias["name"])

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
