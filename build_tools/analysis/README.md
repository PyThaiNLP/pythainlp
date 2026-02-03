# Code Analysis Tools

This directory contains tools for analyzing the PyThaiNLP codebase.

## Type Hint Analysis

### Scripts

#### type_hint_analyzer.py

Main script that performs comprehensive type hint coverage analysis.

**What it does:**

- Scans all Python files in the repository
- Uses Python AST to analyze function and method signatures
- Checks for type hints on parameters and return values
- Categorizes functions by completeness, scope, and priority
- Counts internal references to determine importance
- Maps functions to test suites (core, compact, extra, noauto)
- Runs mypy on each submodule to count type-related errors
- Generates detailed statistics and reports

**Output:**

- Console report with summary statistics
- `output/type_hint_analysis.json` - Detailed JSON data

**Usage:**

```bash
# Run from the build_tools/analysis directory (default output: ./output)
python3 type_hint_analyzer.py

# Or specify a custom output directory
python3 type_hint_analyzer.py --output-dir /path/to/output

# Get help
python3 type_hint_analyzer.py --help
```

#### generate_csv.py

Converts the JSON output from type_hint_analyzer.py into CSV files for easy
analysis.

**Prerequisites:**

- Must run `type_hint_analyzer.py` first to generate the JSON data

**Output:**

- `output/functions_no_hints.csv` - Functions without type hints
- `output/functions_incomplete_hints.csv` - Functions with incomplete hints
- `output/submodule_summary.csv` - Summary by submodule with mypy errors

**Usage:**

```bash
# Run from the build_tools/analysis directory (uses ./output by default)
python3 generate_csv.py

# Or specify custom paths
python3 generate_csv.py --input /path/to/input.json --output-dir /path/to/output

# Get help
python3 generate_csv.py --help
```

### Complete Workflow

To perform a full type hint analysis:

```bash
# Navigate to the analysis directory
cd build_tools/analysis

# 1. Run the analyzer (outputs to ./output by default)
python3 type_hint_analyzer.py

# 2. Generate CSV files (reads from ./output by default)
python3 generate_csv.py

# 3. Review the results
ls -la output/
cat output/submodule_summary.csv
```

### Analysis Categories

**Type Hint Status:**

- **Complete:** All parameters and return value have type hints
- **Incomplete:** Some parameters or return value missing type hints
- **None:** No type hints at all

**Priority Levels:**

- **High:** Public functions with >10 references in core/compact tests
- **Medium:** Public functions with 3-10 references
- **Low:** Private functions or rarely referenced functions

**Test Suites:**

- **core:** Core tests with no external dependencies
- **compact:** Tests with stable, small dependencies
- **extra:** Tests with larger dependencies
- **noauto:** Tests not in CI/CD (e.g., TensorFlow)
- **unknown:** No clear test mapping

### Output Files

All analysis outputs are stored in:

- `build_tools/analysis/output/` - JSON and CSV data files
- `TYPE_HINT_ANALYSIS.md` - Main analysis report (repository root)

## Future Tools

This directory can be extended with additional analysis tools:

- Code complexity analysis
- Documentation coverage analysis
- API stability analysis
- Dependency analysis
