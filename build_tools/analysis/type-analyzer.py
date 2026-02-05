#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Type Annotation Analyzer for PyThaiNLP

This script scans the entire repository and analyzes type annotation coverage
for all functions and classes.

Based on the type completeness information from
https://typing.python.org/en/latest/guides/libraries.html#type-completeness

Usage:
    python type-analyzer.py [--output-dir OUTPUT_DIR]

Options:
    --output-dir    Directory to save output files (default: ./output)
"""
import argparse
import ast
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


def count_mypy_errors_by_submodule(pythainlp_dir: str) -> Dict[str, int]:
    """
    Run mypy on each submodule and count errors.

    :param str pythainlp_dir: Path to pythainlp directory
    :return: Dictionary mapping submodule name to error count
    :rtype: Dict[str, int]
    """
    mypy_errors = {}

    # Get list of submodules
    submodules = []
    for item in os.listdir(pythainlp_dir):
        item_path = os.path.join(pythainlp_dir, item)
        if os.path.isdir(item_path) and not item.startswith(("_", ".")):
            submodules.append(item)

    print("Running mypy on submodules...")

    for submodule in sorted(submodules):
        submodule_path = os.path.join(pythainlp_dir, submodule)
        try:
            # Run mypy on the submodule
            result = subprocess.run(
                ["mypy", submodule_path, "--ignore-missing-imports"],
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Count errors in the output
            # mypy output format: "path/file.py:line: error: message"
            error_count = 0
            for line in result.stdout.split("\n"):
                if ": error:" in line:
                    error_count += 1

            mypy_errors[submodule] = error_count
            print(f"  {submodule}: {error_count} errors")

        except subprocess.TimeoutExpired:
            mypy_errors[submodule] = -1  # Indicate timeout
            print(f"  {submodule}: timeout")
        except FileNotFoundError:
            print("  mypy not found, skipping mypy error counting")
            return {}
        except Exception as e:
            mypy_errors[submodule] = -1  # Indicate error
            print(f"  {submodule}: error ({e})")

    return mypy_errors


class TypeHintAnalyzer(ast.NodeVisitor):
    """Analyzes Python files for type hint coverage."""

    def __init__(self, filepath: str, module_path: str):
        self.filepath = filepath
        self.module_path = module_path
        self.results = []
        self.current_class = None
        self.current_function = None
        self.module_level = True

    def is_private(self, name: str) -> bool:
        """Check if a name is private (starts with underscore)."""
        return name.startswith("_") and not (
            name.startswith("__") and name.endswith("__")
        )

    def is_public(self, name: str) -> bool:
        """Check if a name is public."""
        return not self.is_private(name)

    def check_function_type_hints(
        self, node: ast.FunctionDef
    ) -> Tuple[str, int, int]:
        """
        Check type hint completeness for a function.
        Returns: (status, total_params, hinted_params)
        - status: "complete", "incomplete", "none"
        - total_params: number of parameters (excluding self/cls)
        - hinted_params: number of parameters with type hints
        """
        # Count parameters (excluding self/cls)
        params = []
        for arg in node.args.args:
            if arg.arg not in ("self", "cls"):
                params.append(arg)

        total_params = len(params)
        hinted_params = sum(1 for arg in params if arg.annotation is not None)
        has_return_hint = node.returns is not None

        # Determine status
        if total_params == 0 and not has_return_hint:
            status = "none"
        elif total_params == 0 and has_return_hint:
            status = "complete"
        elif hinted_params == 0 and not has_return_hint:
            status = "none"
        elif hinted_params == total_params and has_return_hint:
            status = "complete"
        else:
            status = "incomplete"

        return status, total_params, hinted_params, has_return_hint

    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return (
                f"{self._get_decorator_name(decorator.value)}"
                f".{decorator.attr}"
            )
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        else:
            return "unknown"

    def _is_type_alias(self, node: ast.AnnAssign) -> bool:
        """Check if an annotated assignment is a type alias."""
        if node.annotation is None:
            return False

        # Check for TypeAlias annotation
        ann_is_type_alias = (
            isinstance(node.annotation, ast.Name)
            and node.annotation.id == "TypeAlias"
        )
        if ann_is_type_alias:
            return True

        # Check for typing.TypeAlias or typing_extensions.TypeAlias
        if isinstance(node.annotation, ast.Attribute):
            if node.annotation.attr == "TypeAlias":
                return True

        return False

    def _is_instance_variable(self, target: ast.expr) -> bool:
        """Check if target is an instance variable (self.attr)."""
        return (
            isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "self"
        )

    def _get_variable_name(self, target: ast.expr) -> str:
        """Extract variable name from assignment target."""
        if isinstance(target, ast.Name):
            return target.id
        elif isinstance(target, ast.Attribute):
            return target.attr
        else:
            return "unknown"

    def visit_AnnAssign(self, node: ast.AnnAssign):
        """Visit annotated assignment (variable with type hint)."""
        # Skip if we're in a function/method body (local variables)
        in_func_not_inst = (
            self.current_function is not None
            and not self._is_instance_variable(node.target)
        )
        if in_func_not_inst:
            self.generic_visit(node)
            return

        var_name = self._get_variable_name(node.target)

        # Determine variable type and qualified name
        if self._is_type_alias(node):
            var_type = "type_alias"
            qualified_name = f"{self.module_path}.{var_name}"
            scope = "private" if self.is_private(var_name) else "public"
            status = "complete"  # Type aliases always have annotations
        elif self._is_instance_variable(node.target):
            var_type = "instance_variable"
            qualified_name = (
                f"{self.module_path}.{self.current_class}.{var_name}"
            )
            scope = "private" if self.is_private(var_name) else "public"
            status = "complete"  # Has type hint
        elif self.current_class is not None and self.current_function is None:
            var_type = "class_variable"
            qualified_name = (
                f"{self.module_path}.{self.current_class}.{var_name}"
            )
            scope = "private" if self.is_private(var_name) else "public"
            status = "complete"  # Has type hint
        elif self.module_level:
            var_type = "module_variable"
            qualified_name = f"{self.module_path}.{var_name}"
            scope = "private" if self.is_private(var_name) else "public"
            status = "complete"  # Has type hint
        else:
            # Local variable, skip
            self.generic_visit(node)
            return

        result = {
            "type": var_type,
            "name": var_name,
            "qualified_name": qualified_name,
            "scope": scope,
            "status": status,
            "line": node.lineno,
            "parent_class": (
                self.current_class
                if var_type in ("class_variable", "instance_variable")
                else None
            ),
        }

        self.results.append(result)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """Visit regular assignment (variable without type hint)."""
        # Skip if we're in a function/method body (local variables)
        # Instance variables without hints are handled here
        is_instance_var = False
        for target in node.targets:
            if self._is_instance_variable(target):
                is_instance_var = True
                break

        if self.current_function is not None and not is_instance_var:
            self.generic_visit(node)
            return

        for target in node.targets:
            var_name = self._get_variable_name(target)

            # Determine variable type and qualified name
            if self._is_instance_variable(target):
                var_type = "instance_variable"
                qualified_name = (
                    f"{self.module_path}.{self.current_class}.{var_name}"
                )
                scope = "private" if self.is_private(var_name) else "public"
                status = "none"  # No type hint
            elif (
                self.current_class is not None
                and self.current_function is None
            ):
                var_type = "class_variable"
                qualified_name = (
                    f"{self.module_path}.{self.current_class}.{var_name}"
                )
                scope = "private" if self.is_private(var_name) else "public"
                status = "none"  # No type hint
            elif self.module_level:
                var_type = "module_variable"
                qualified_name = f"{self.module_path}.{var_name}"
                scope = "private" if self.is_private(var_name) else "public"
                status = "none"  # No type hint
            else:
                # Local variable, skip
                continue

            result = {
                "type": var_type,
                "name": var_name,
                "qualified_name": qualified_name,
                "scope": scope,
                "status": status,
                "line": node.lineno,
                "parent_class": (
                    self.current_class
                    if var_type in ("class_variable", "instance_variable")
                    else None
                ),
            }

            self.results.append(result)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definition."""
        status, total_params, hinted_params, has_return = (
            self.check_function_type_hints(node)
        )

        scope = "private" if self.is_private(node.name) else "public"

        # Check decorators
        decorators_info = []
        for decorator in node.decorator_list:
            dec_name = self._get_decorator_name(decorator)
            decorators_info.append(dec_name)

        result = {
            "type": "function",
            "name": node.name,
            "qualified_name": (
                f"{self.module_path}.{self.current_class}.{node.name}"
                if self.current_class
                else f"{self.module_path}.{node.name}"
            ),
            "scope": scope,
            "status": status,
            "line": node.lineno,
            "total_params": total_params,
            "hinted_params": hinted_params,
            "has_return": has_return,
            "is_method": self.current_class is not None,
            "parent_class": self.current_class,
            "decorators": decorators_info,
        }

        self.results.append(result)

        # Track that we're inside a function
        old_function = self.current_function
        self.current_function = node.name
        old_module_level = self.module_level
        self.module_level = False
        self.generic_visit(node)
        self.current_function = old_function
        self.module_level = old_module_level

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visit async function definition."""
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definition."""
        scope = "private" if self.is_private(node.name) else "public"

        result = {
            "type": "class",
            "name": node.name,
            "qualified_name": f"{self.module_path}.{node.name}",
            "scope": scope,
            "status": "N/A",  # Classes don't have type hints themselves
            "line": node.lineno,
        }

        self.results.append(result)

        # Visit class body (methods and class variables)
        old_class = self.current_class
        self.current_class = node.name
        old_module_level = self.module_level
        self.module_level = False
        self.generic_visit(node)
        self.current_class = old_class
        self.module_level = old_module_level


def find_python_files(root_dir: str) -> List[str]:
    """Find all Python files in the given directory."""
    python_files = []
    root_path = Path(root_dir)

    for py_file in root_path.rglob("*.py"):
        # Skip build, dist, .git, and other non-source directories
        parts = py_file.parts
        skip_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "build",
            "dist",
            ".eggs",
            "*.egg-info",
            ".tox",
            ".venv",
            "venv",
        }

        if any(skip_dir in parts for skip_dir in skip_dirs):
            continue

        python_files.append(str(py_file))

    return sorted(python_files)


def get_module_path(filepath: str, root_dir: str) -> str:
    """Convert file path to module path."""
    rel_path = os.path.relpath(filepath, root_dir)
    module_path = rel_path.replace(os.sep, ".").replace(".py", "")

    if module_path.endswith(".__init__"):
        module_path = module_path[:-9]

    return module_path


def analyze_file(filepath: str, root_dir: str) -> List[Dict[str, Any]]:
    """Analyze a single Python file for type hints."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=filepath)
        module_path = get_module_path(filepath, root_dir)

        analyzer = TypeHintAnalyzer(filepath, module_path)
        analyzer.visit(tree)

        return analyzer.results
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}", file=sys.stderr)
        return []


def get_submodule(qualified_name: str) -> str:
    """Extract submodule from qualified name."""
    parts = qualified_name.split(".")
    if len(parts) > 2 and parts[0] == "pythainlp":
        return parts[1]
    elif len(parts) > 1:
        return parts[0]
    return "root"


def count_references(qualified_name: str, all_files: List[str]) -> int:
    """Count how many times a name is referenced in the codebase."""
    count = 0
    name_parts = qualified_name.split(".")
    search_name = name_parts[-1]

    for filepath in all_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Simple text search - not perfect but gives an approximation
                count += content.count(search_name)
        except Exception:
            pass

    return count


def get_test_suite(filepath: str, tests_dir: str) -> str:
    """Determine which test suite a test file belongs to."""
    if not filepath.startswith(tests_dir):
        return "not_in_tests"

    filename = os.path.basename(filepath)

    if filename.startswith("test_") and not filename.startswith(
        ("testc_", "testx_", "testn_")
    ):
        return "core"
    elif filename.startswith("testc_"):
        return "compact"
    elif filename.startswith("testx_"):
        return "extra"
    elif filename.startswith("testn_"):
        return "noauto"
    else:
        return "other"


def find_corresponding_test_suite(
    qualified_name: str, all_results: List[Dict]
) -> str:
    """Find which test suite tests this function/class."""
    # Look for test functions that reference this name
    test_suites = set()

    name_parts = qualified_name.split(".")
    search_name = name_parts[-1]

    for result in all_results:
        if "tests." in result["qualified_name"]:
            # This is a test function
            test_suite = get_test_suite(result.get("filepath", ""), "tests")
            # Simple heuristic: if test name contains the function name,
            # it likely tests it
            if search_name.lower() in result["name"].lower():
                test_suites.add(test_suite)

    if test_suites:
        # Prioritize: core > compact > extra > noauto
        priority_order = ["core", "compact", "extra", "noauto", "other"]
        for suite in priority_order:
            if suite in test_suites:
                return suite

    return "unknown"


def assign_priority(result: Dict) -> str:
    """Assign priority based on scope, references, and test suite."""
    scope = result.get("scope", "private")
    refs = result.get("references", 0)
    test_suite = result.get("test_suite", "unknown")

    # Public functions with many references in core tests: high priority
    if scope == "public" and refs > 10 and test_suite in ("core", "compact"):
        return "high"
    # Public functions with some references: medium priority
    elif scope == "public" and refs > 3:
        return "medium"
    # Everything else: low priority
    else:
        return "low"


def main():
    """Main function to analyze type hints across the repository."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Analyze type hint coverage in PyThaiNLP"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to save output files (default: ./output)",
    )
    args = parser.parse_args()

    # Auto-detect repository root (go up from script location)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    pythainlp_dir = repo_root / "pythainlp"
    tests_dir = repo_root / "tests"

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = script_dir / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("TYPE ANNOTATION COVERAGE ANALYSIS FOR PYTHAINLP")
    print("=" * 80)
    print()
    print(f"Repository root: {repo_root}")
    print(f"Output directory: {output_dir}")
    print()

    # Find all Python files
    print("Scanning Python files...")
    pythainlp_files = find_python_files(str(pythainlp_dir))
    test_files = find_python_files(str(tests_dir))
    all_files = pythainlp_files + test_files

    print(f"Found {len(pythainlp_files)} Python files in pythainlp/")
    print(f"Found {len(test_files)} Python files in tests/")
    print()

    # Analyze all files
    print("Analyzing type hints...")
    all_results = []

    for filepath in pythainlp_files:
        results = analyze_file(filepath, str(repo_root))
        for result in results:
            result["filepath"] = filepath
            result["in_tests"] = False
        all_results.extend(results)

    for filepath in test_files:
        results = analyze_file(filepath, str(repo_root))
        for result in results:
            result["filepath"] = filepath
            result["in_tests"] = True
            result["test_suite"] = get_test_suite(filepath, str(tests_dir))
        all_results.extend(results)

    # Count mypy errors by submodule
    print()
    mypy_errors = count_mypy_errors_by_submodule(str(pythainlp_dir))
    print()

    # Count references and assign test suites for non-test files
    print("Counting references and determining test coverage...")
    for result in all_results:
        if not result.get("in_tests", False):
            result["references"] = count_references(
                result["qualified_name"], all_files
            )
            result["test_suite"] = find_corresponding_test_suite(
                result["qualified_name"], all_results
            )
            result["priority"] = assign_priority(result)

    # Separate by type
    functions = [
        r
        for r in all_results
        if r["type"] == "function" and not r.get("in_tests", False)
    ]
    classes = [
        r
        for r in all_results
        if r["type"] == "class" and not r.get("in_tests", False)
    ]
    class_vars = [
        r
        for r in all_results
        if r["type"] == "class_variable" and not r.get("in_tests", False)
    ]
    instance_vars = [
        r
        for r in all_results
        if r["type"] == "instance_variable" and not r.get("in_tests", False)
    ]
    module_vars = [
        r
        for r in all_results
        if r["type"] == "module_variable" and not r.get("in_tests", False)
    ]
    type_aliases = [
        r
        for r in all_results
        if r["type"] == "type_alias" and not r.get("in_tests", False)
    ]

    print(f"Analyzed {len(functions)} functions/methods")
    print(f"Analyzed {len(classes)} classes")
    print(f"Analyzed {len(class_vars)} class variables")
    print(f"Analyzed {len(instance_vars)} instance variables")
    print(f"Analyzed {len(module_vars)} module variables")
    print(f"Analyzed {len(type_aliases)} type aliases")
    print()

    # Calculate statistics for functions
    complete = [f for f in functions if f["status"] == "complete"]
    incomplete = [f for f in functions if f["status"] == "incomplete"]
    none = [f for f in functions if f["status"] == "none"]

    total = len(functions)
    pct_complete = (len(complete) / total * 100) if total > 0 else 0
    pct_incomplete = (len(incomplete) / total * 100) if total > 0 else 0
    pct_none = (len(none) / total * 100) if total > 0 else 0

    print("=" * 80)
    print("OVERALL STATISTICS - FUNCTIONS/METHODS")
    print("=" * 80)
    print(f"Total functions/methods: {total}")
    print(
        f"Complete type hints:     {len(complete):4d} "
        f"({pct_complete:5.2f}%)"
    )
    print(
        f"Incomplete type hints:   {len(incomplete):4d} "
        f"({pct_incomplete:5.2f}%)"
    )
    print(f"No type hints:           {len(none):4d} ({pct_none:5.2f}%)")
    print()

    # Calculate statistics for variables
    all_vars = class_vars + instance_vars + module_vars
    vars_complete = [v for v in all_vars if v["status"] == "complete"]
    vars_none = [v for v in all_vars if v["status"] == "none"]

    total_vars = len(all_vars)
    pct_vars_complete = (
        (len(vars_complete) / total_vars * 100) if total_vars > 0 else 0
    )
    pct_vars_none = (
        (len(vars_none) / total_vars * 100) if total_vars > 0 else 0
    )

    print("=" * 80)
    print("OVERALL STATISTICS - VARIABLES")
    print("=" * 80)
    print(f"Total variables:         {total_vars}")
    print(f"  Class variables:       {len(class_vars)}")
    print(f"  Instance variables:    {len(instance_vars)}")
    print(f"  Module variables:      {len(module_vars)}")
    print(
        f"Complete type hints:     {len(vars_complete):4d} "
        f"({pct_vars_complete:5.2f}%)"
    )
    print(
        f"No type hints:           {len(vars_none):4d} "
        f"({pct_vars_none:5.2f}%)"
    )
    print()

    print("=" * 80)
    print("STATISTICS - TYPE ALIASES")
    print("=" * 80)
    print(f"Total type aliases:      {len(type_aliases)}")
    print()

    # Group by submodule
    by_submodule = defaultdict(
        lambda: {"complete": [], "incomplete": [], "none": []}
    )
    for func in functions:
        submodule = get_submodule(func["qualified_name"])
        by_submodule[submodule][func["status"]].append(func)

    print("=" * 80)
    print("BREAKDOWN BY SUBMODULE")
    print("=" * 80)

    for submodule in sorted(by_submodule.keys()):
        data = by_submodule[submodule]
        total_sub = (
            len(data["complete"])
            + len(data["incomplete"])
            + len(data["none"])
        )
        pct_comp = (
            (len(data["complete"]) / total_sub * 100) if total_sub > 0 else 0
        )
        pct_inc = (
            (len(data["incomplete"]) / total_sub * 100)
            if total_sub > 0
            else 0
        )
        pct_no = (
            (len(data["none"]) / total_sub * 100) if total_sub > 0 else 0
        )

        mypy_err_str = ""
        if submodule in mypy_errors:
            if mypy_errors[submodule] >= 0:
                mypy_err_str = f", Mypy errors: {mypy_errors[submodule]}"
            elif mypy_errors[submodule] == -1:
                mypy_err_str = ", Mypy: error/timeout"

        print(f"\n{submodule}:")
        print(f"  Total: {total_sub}{mypy_err_str}")
        print(f"  Complete:   {len(data['complete']):4d} ({pct_comp:5.2f}%)")
        print(f"  Incomplete: {len(data['incomplete']):4d} ({pct_inc:5.2f}%)")
        print(f"  None:       {len(data['none']):4d} ({pct_no:5.2f}%)")

    print()
    print("=" * 80)
    print("FUNCTIONS/METHODS WITHOUT TYPE HINTS (sorted by priority)")
    print("=" * 80)

    # Sort by priority, then by references
    none_sorted = sorted(
        none,
        key=lambda x: (
            {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 2),
            -x.get("references", 0),
        ),
    )

    print(
        "\nHIGH PRIORITY "
        "(public, frequently referenced, in core/compact tests):"
    )
    print("-" * 80)
    for func in none_sorted:
        if func.get("priority") == "high":
            print(f"  {func['qualified_name']}")
            print(
                f"    Scope: {func['scope']}, "
                f"References: {func.get('references', 0)}, "
                f"Test suite: {func.get('test_suite', 'unknown')}"
            )
            print(f"    File: {func['filepath']}:{func['line']}")
            print()

    print("\nMEDIUM PRIORITY (public, some references):")
    print("-" * 80)
    count = 0
    for func in none_sorted:
        if func.get("priority") == "medium":
            if count < 20:  # Limit output
                print(f"  {func['qualified_name']}")
                print(
                    f"    Scope: {func['scope']}, "
                    f"References: {func.get('references', 0)}, "
                    f"Test suite: {func.get('test_suite', 'unknown')}"
                )
            count += 1
    if count > 20:
        print(f"  ... and {count - 20} more")
    print()

    print("\nLOW PRIORITY (private or rarely referenced):")
    print("-" * 80)
    low_count = sum(1 for f in none_sorted if f.get("priority") == "low")
    print(f"  Total: {low_count} functions")
    print()

    print("=" * 80)
    print(
        "FUNCTIONS/METHODS WITH INCOMPLETE TYPE HINTS (sorted by priority)"
    )
    print("=" * 80)

    incomplete_sorted = sorted(
        incomplete,
        key=lambda x: (
            {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 2),
            -x.get("references", 0),
        ),
    )

    print("\nHIGH PRIORITY:")
    print("-" * 80)
    for func in incomplete_sorted:
        if func.get("priority") == "high":
            print(f"  {func['qualified_name']}")
            print(
                f"    Scope: {func['scope']}, "
                f"Params: {func['hinted_params']}/{func['total_params']}, "
                f"Return: {func['has_return']}"
            )
            print(
                f"    References: {func.get('references', 0)}, "
                f"Test suite: {func.get('test_suite', 'unknown')}"
            )
            print(f"    File: {func['filepath']}:{func['line']}")
            print()

    print("\nMEDIUM PRIORITY:")
    print("-" * 80)
    count = 0
    for func in incomplete_sorted:
        if func.get("priority") == "medium":
            if count < 20:
                print(f"  {func['qualified_name']}")
                print(
                    f"    Params: {func['hinted_params']}/"
                    f"{func['total_params']}, "
                    f"Return: {func['has_return']}"
                )
            count += 1
    if count > 20:
        print(f"  ... and {count - 20} more")
    print()

    print("\nLOW PRIORITY:")
    print("-" * 80)
    low_count = sum(1 for f in incomplete_sorted if f.get("priority") == "low")
    print(f"  Total: {low_count} functions")
    print()

    # Save detailed results to JSON
    output_file = output_dir / "type_hint_analysis.json"
    with open(output_file, "w") as f:
        json.dump(
            {
                "statistics": {
                    "functions": {
                        "total": total,
                        "complete": len(complete),
                        "incomplete": len(incomplete),
                        "none": len(none),
                        "pct_complete": pct_complete,
                        "pct_incomplete": pct_incomplete,
                        "pct_none": pct_none,
                    },
                    "variables": {
                        "total": total_vars,
                        "complete": len(vars_complete),
                        "none": len(vars_none),
                        "pct_complete": pct_vars_complete,
                        "pct_none": pct_vars_none,
                        "class_variables": len(class_vars),
                        "instance_variables": len(instance_vars),
                        "module_variables": len(module_vars),
                    },
                    "type_aliases": {
                        "total": len(type_aliases),
                    },
                    "classes": {
                        "total": len(classes),
                    },
                },
                "by_submodule": {
                    k: {
                        "complete": len(v["complete"]),
                        "incomplete": len(v["incomplete"]),
                        "none": len(v["none"]),
                        "mypy_errors": mypy_errors.get(k, 0),
                    }
                    for k, v in by_submodule.items()
                },
                "functions_no_hints": [
                    {
                        "name": f["qualified_name"],
                        "scope": f["scope"],
                        "references": f.get("references", 0),
                        "test_suite": f.get("test_suite", "unknown"),
                        "priority": f.get("priority", "low"),
                        "file": f["filepath"],
                        "line": f["line"],
                        "decorators": f.get("decorators", []),
                    }
                    for f in none_sorted
                ],
                "functions_incomplete_hints": [
                    {
                        "name": f["qualified_name"],
                        "scope": f["scope"],
                        "params": f'{f["hinted_params"]}/{f["total_params"]}',
                        "return": f["has_return"],
                        "references": f.get("references", 0),
                        "test_suite": f.get("test_suite", "unknown"),
                        "priority": f.get("priority", "low"),
                        "file": f["filepath"],
                        "line": f["line"],
                        "decorators": f.get("decorators", []),
                    }
                    for f in incomplete_sorted
                ],
                "class_variables_no_hints": [
                    {
                        "name": v["qualified_name"],
                        "scope": v["scope"],
                        "parent_class": v.get("parent_class"),
                        "file": v["filepath"],
                        "line": v["line"],
                    }
                    for v in class_vars if v["status"] == "none"
                ],
                "instance_variables_no_hints": [
                    {
                        "name": v["qualified_name"],
                        "scope": v["scope"],
                        "parent_class": v.get("parent_class"),
                        "file": v["filepath"],
                        "line": v["line"],
                    }
                    for v in instance_vars if v["status"] == "none"
                ],
                "module_variables_no_hints": [
                    {
                        "name": v["qualified_name"],
                        "scope": v["scope"],
                        "file": v["filepath"],
                        "line": v["line"],
                    }
                    for v in module_vars if v["status"] == "none"
                ],
                "type_aliases": [
                    {
                        "name": t["qualified_name"],
                        "scope": t["scope"],
                        "file": t["filepath"],
                        "line": t["line"],
                    }
                    for t in type_aliases
                ],
            },
            f,
            indent=2,
        )

    print(f"Detailed results saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
