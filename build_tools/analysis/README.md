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
- Analyzes class variables, instance variables, and module variables
- Detects type aliases (TypeAlias annotations)
- Tracks decorators used on functions and methods
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
- `output/class_variables_no_hints.csv` - Class variables without type hints
- `output/instance_variables_no_hints.csv` - Instance variables without type hints
- `output/module_variables_no_hints.csv` - Module variables without type hints
- `output/type_aliases.csv` - Type aliases defined in the codebase
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

### Type Completeness Standards

This analyzer follows the type completeness guidelines from the Python typing documentation:
https://typing.python.org/en/latest/guides/libraries.html#type-completeness

The analysis covers:
- All function and method signatures (parameters and return types)
- Class variables (class-level attributes)
- Instance variables (instance attributes)
- Module-level variables
- Type aliases
- Decorator information for functions and methods

### Analysis Categories

**Type Hint Status:**

- **Complete:** All parameters and return value have type hints (for functions), or variable has type annotation (for variables)
- **Incomplete:** Some parameters or return value missing type hints (for functions only)
- **None:** No type hints at all

**Analyzed Elements:**

- **Functions/Methods:** Function signatures including parameters and return types
- **Class Variables:** Variables defined at class level
- **Instance Variables:** Variables defined as instance attributes (e.g., `self.attr`)
- **Module Variables:** Variables defined at module level
- **Type Aliases:** Type alias definitions (using TypeAlias annotation)
- **Decorators:** Decorators applied to functions and methods

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
