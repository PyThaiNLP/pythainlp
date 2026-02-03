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
- Generates detailed statistics and reports

**Output:**

- Console report with summary statistics
- `/tmp/type_hint_analysis.json` - Detailed JSON data

**Usage:**

```bash
python3 build_tools/analysis/type_hint_analyzer.py
```

#### generate_csv.py

Converts the JSON output from type_hint_analyzer.py into CSV files for easy analysis.

**Prerequisites:**

- Must run `type_hint_analyzer.py` first to generate the JSON data

**Output:**

- `/tmp/functions_no_hints.csv` - Functions without type hints
- `/tmp/functions_incomplete_hints.csv` - Functions with incomplete hints
- `/tmp/submodule_summary.csv` - Summary by submodule

**Usage:**

```bash
python3 build_tools/analysis/generate_csv.py
```

### Complete Workflow

To perform a full type hint analysis and update the documentation:

```bash
# Run from repository root
cd /path/to/pythainlp

# 1. Run the analyzer
python3 build_tools/analysis/type_hint_analyzer.py > TYPE_HINT_ANALYSIS_LATEST.txt

# 2. Generate CSV files
python3 build_tools/analysis/generate_csv.py

# 3. Copy CSV files to docs
cp /tmp/*.csv docs/type_hint_analysis/

# 4. Review the results
cat TYPE_HINT_ANALYSIS_LATEST.txt
cat docs/type_hint_analysis/submodule_summary.csv
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

- `docs/type_hint_analysis/` - CSV data files and README
- `TYPE_HINT_ANALYSIS.md` - Main analysis report (repository root)

## Future Tools

This directory can be extended with additional analysis tools:

- Code complexity analysis
- Documentation coverage analysis
- API stability analysis
- Dependency analysis
