# Code analysis tools

This directory contains tools for analyzing the PyThaiNLP codebase.

## Type annotation analysis

### Overview

The type annotation analysis system provides comprehensive coverage analysis
of type annotations across the entire PyThaiNLP codebase.
It follows the
[Python typing documentation's type completeness guidelines][type-completeness]
to estimate the quality and completeness of type annotations.

[type-completeness]: https://typing.python.org/en/latest/guides/libraries.html#type-completeness

### Scripts

#### type-analyzer.py

Main script that performs comprehensive type annotation coverage analysis
using Python's Abstract Syntax Tree (AST) module.

**What it analyzes:**

- **Functions and Methods**: Parameter types, return types, and completeness status
- **Class Variables**: Class-level attributes with or without type annotations
- **Instance Variables**: Instance attributes (`self.attr`) with or without annotations
- **Module Variables**: Module-level variables and constants
- **Type Aliases**: TypeAlias definitions (`MyType: TypeAlias = dict[str, int]`)
- **Decorators**: Tracks decorator usage on functions and methods
- **Test Coverage**: Maps functions to test suites (core, compact, extra, noauto)
- **Code Usage**: Counts internal references to determine importance
- **Type Checker Errors**: Runs mypy on each submodule to count type-related errors

**Implementation Details:**

The analyzer uses Python's `ast` module to parse and traverse the syntax tree
of each Python file. Key components:

- `TypeHintAnalyzer` class: Custom `ast.NodeVisitor` that visits each node
- `visit_FunctionDef()`: Analyzes function/method signatures
- `visit_ClassDef()`: Tracks class context for variable analysis
- `visit_AnnAssign()`: Handles annotated assignments (variables with type hints)
- `visit_Assign()`: Handles non-annotated assignments for comparison

The analyzer distinguishes between:

- Module-level scope (top of file)
- Class-level scope (inside class definition)
- Function-level scope (inside function/method)
- Instance scope (self.attr assignments)

**Output:**

- Console report with summary statistics and priority-sorted listings
- `output/type_hint_analysis.json` - Detailed JSON data with all analysis results

**Usage:**

For best results, delete all previous data files (`*.csv`, `*.json`)
and clear the cache for mypy and any other static type checkers
before running the analyzer.

```bash
# Run from the build_tools/analysis directory (default output: ./output)
python type-analyzer.py

# Or specify a custom output directory
python type-analyzer.py --output-dir /path/to/output

# Get help
python type-analyzer.py --help
```

Enable more accurate static analysis by installing optional dependencies
(and their type stubs, if available) for enhanced type discovery.

#### gen-csv.py

Converts the JSON output from type-analyzer.py into CSV files for
easy analysis in spreadsheet applications or data analysis tools.

**Prerequisites:**

- Must run `type-analyzer.py` first to generate the JSON data

**Output:**

- `output/functions_no_hints.csv` - Functions without any type hints
- `output/functions_incomplete_hints.csv` - Functions with partial hints
- `output/class_variables_no_hints.csv` - Class variables without type hints
- `output/instance_variables_no_hints.csv` - Instance variables without type hints
- `output/module_variables_no_hints.csv` - Module variables without type hints
- `output/type_aliases.csv` - All type aliases defined in the codebase
- `output/submodule_summary.csv` - Summary statistics by submodule with mypy errors

**CSV Schema:**

Functions CSV files include:

- Function Name (qualified name)
- Submodule
- Scope (public/private)
- Priority (high/medium/low)
- Parameters Hinted (for incomplete)
- Has Return Type
- References (usage count)
- Test Suite
- Decorators
- File Path
- Line Number

Variables CSV files include:

- Variable Name (qualified name)
- Submodule
- Parent Class (for class/instance variables)
- Scope (public/private)
- File Path
- Line Number

**Usage:**

```bash
# Run from the build_tools/analysis directory (uses ./output by default)
python gen-csv.py

# Or specify custom paths
python gen-csv.py --input /path/to/input.json --output-dir /path/to/output

# Get help
python gen-csv.py --help
```

### Complete Workflow

To perform a full type annotation analysis:

```bash
# Navigate to the analysis directory
cd build_tools/analysis

# 1. Run the analyzer (outputs to ./output by default)
python type-analyzer.py

# 2. Generate CSV files (reads from ./output by default)
python gen-csv.py

# 3. Review the results
ls -la output/
cat output/submodule_summary.csv
```

**Example Output:**

```text
================================================================================
TYPE ANNOTATION COVERAGE ANALYSIS FOR PYTHAINLP
================================================================================

Repository root: /path/to/pythainlp
Output directory: ./output

Scanning Python files...
Found 191 Python files in pythainlp/
Found 55 Python files in tests/

Analyzing type hints...

Running mypy on submodules...
  ancient: 0 errors
  augment: 5 errors
  ...

Counting references and determining test coverage...
Analyzed 720 functions/methods
Analyzed 96 classes
Analyzed 25 class variables
Analyzed 426 instance variables
Analyzed 508 module variables
Analyzed 0 type aliases

================================================================================
OVERALL STATISTICS - FUNCTIONS/METHODS
================================================================================
Total functions/methods: 720
Complete type hints:      592 (82.22%)
Incomplete type hints:     56 ( 7.78%)
No type hints:             72 (10.00%)

================================================================================
OVERALL STATISTICS - VARIABLES
================================================================================
Total variables:         959
  Class variables:       25
  Instance variables:    426
  Module variables:      508
Complete type hints:       50 ( 5.21%)
No type hints:            909 (94.79%)
```

### Automated Analysis

The repository includes a GitHub Actions workflow that automatically runs the type hint analyzer on every push to the `dev` branch:

- **Workflow**: `.github/workflows/type-hint-analysis.yml`
- **Trigger**: Push to `dev` branch
- **Environment**: ubuntu-latest, Python 3.9
- **Artifacts**: JSON and CSV files (30-day retention)
- **Summary**: Displayed in GitHub Actions UI

The workflow provides continuous monitoring of type hint coverage as the codebase evolves.

### Type Completeness Standards

This analyzer follows the type completeness guidelines from the Python typing documentation:
<https://typing.python.org/en/latest/guides/libraries.html#type-completeness>

The analysis covers:

- All function and method signatures (parameters and return types)
- Class variables (class-level attributes)
- Instance variables (instance attributes)
- Module-level variables
- Type aliases
- Decorator information for functions and methods

**Type Completeness Criteria:**

According to PEP 561 and the Python typing documentation,
a library is considered to have complete type hints when:

1. All exported functions, methods, and classes have type annotations
2. All public module-level variables have type annotations
3. All class and instance variables in exported classes have type annotations
4. Generic types are properly parameterized
5. The library passes type checking with mypy in strict mode

### Analysis categories

**Type hint status:**

- **Complete:** All parameters and return value have type hints (for functions), or variable has type annotation (for variables)
- **Incomplete:** Some parameters or return value missing type hints (for functions only)
- **None:** No type hints at all

**Analyzed Elements:**

- **Functions/Methods:** Function signatures including parameters and return types
  - Excludes `self` and `cls` parameters from parameter counts
  - Considers both parameters and return type for completeness
  - Tracks decorator usage (e.g., `@staticmethod`, `@lru_cache`)
  
- **Class Variables:** Variables defined at class level
  - Distinguishes between annotated (`class_var: int = 10`) and non-annotated
  - Can include `ClassVar` type hints for class-specific attributes
  
- **Instance Variables:** Variables defined as instance attributes (e.g., `self.attr`)
  - Detected in `__init__` and other methods
  - Tracks both annotated (`self.x: int = 5`) and non-annotated assignments
  
- **Module Variables:** Variables defined at module level
  - Includes constants, configuration values, and exported names
  - Important for library API clarity
  
- **Type Aliases:** Type alias definitions (using TypeAlias annotation)
  - Modern syntax: `MyType: TypeAlias = dict[str, int]`
  - Also detects `typing.TypeAlias` and `typing_extensions.TypeAlias`

**Priority levels:**

Functions are assigned priority based on visibility and usage patterns:

- **High:** Public functions with >10 references in core/compact tests
  - Most critical for library users
  - Should be prioritized for type hint additions
  
- **Medium:** Public functions with 3-10 references
  - Important but less frequently used
  
- **Low:** Private functions or rarely referenced functions
  - Internal implementation details
  - Lower priority for type hint coverage

**Test suites:**

The analyzer maps functions to test categories based on their dependencies:

- **core:** Core tests with no external dependencies
- **compact:** Tests with stable, small dependencies
- **extra:** Tests with larger dependencies
- **noauto:** Tests not in CI/CD (e.g., TensorFlow)
- **unknown:** No clear test mapping

This mapping helps understand which functions are tested and their dependency requirements.

### Output files

All analysis outputs are stored in:

- `build_tools/analysis/output/` - JSON and CSV data files

**JSON structure:**

```json
{
  "statistics": {
    "functions": {
      "total": 720,
      "complete": 592,
      "incomplete": 56,
      "none": 72,
      "pct_complete": 82.22,
      "pct_incomplete": 7.78,
      "pct_none": 10.00
    },
    "variables": {
      "total": 959,
      "complete": 50,
      "none": 909,
      "pct_complete": 5.21,
      "pct_none": 94.79,
      "class_variables": 25,
      "instance_variables": 426,
      "module_variables": 508
    },
    "type_aliases": {
      "total": 0
    },
    "classes": {
      "total": 96
    }
  },
  "by_submodule": { ... },
  "functions_no_hints": [ ... ],
  "functions_incomplete_hints": [ ... ],
  "class_variables_no_hints": [ ... ],
  "instance_variables_no_hints": [ ... ],
  "module_variables_no_hints": [ ... ],
  "type_aliases": [ ... ]
}
```

### Code review and quality

**Documentation coverage:**

The analyzer codebase maintains high documentation standards:

- 95.7% docstring coverage (22 of 23 functions/methods)
- All public functions have comprehensive docstrings
- Docstrings follow reStructuredText format for Sphinx compatibility

**Code quality:**

- Follows Ruff linting standards
- Type hints on all function signatures
- Clear separation of concerns with dedicated helper methods
- Proper exception handling for file I/O and subprocess calls

**Key Design decisions:**

1. **AST-based Analysis**: Uses Python's `ast` module rather than runtime inspection
   - Pros: No need to import/execute code, faster, safer
   - Cons: Cannot detect dynamically generated code

2. **Stateful Visitor Pattern**: Tracks context (class, function, module level)
   - Enables accurate classification of variables
   - Distinguishes between local, instance, class, and module variables

3. **Reference Counting**: Simple text-based search for usage patterns
   - Fast and implementation-agnostic
   - Trade-off: May have false positives (comments, strings)

4. **Priority System**: Heuristic-based prioritization
   - Helps focus improvement efforts on most impactful areas
   - Based on visibility (public/private) and usage frequency

**Limitations:**

1. TypeAlias detection requires explicit annotation (PEP 613 style)
2. Does not detect type aliases using the old `Type[...]` pattern
3. Reference counting may be inflated by matches in comments/docstrings
4. Mypy analysis is optional and skipped if mypy is not installed
5. Cannot analyze dynamically generated code or runtime type additions

### Potential Improvements

**Enhancements for Future Versions:**

1. **Enhanced TypeAlias Detection**
   - Support for old-style type aliases without TypeAlias annotation
   - Detection of generic type aliases (e.g., `List[T]`, `Dict[K, V]`)

2. **More Accurate Reference Counting**
   - Use AST-based import analysis instead of text search
   - Track actual usage vs. string mentions
   - Distinguish between different types of references (call, attribute access, etc.)

3. **Additional Metrics**
   - Generic type parameterization completeness
   - Protocol and ABC coverage
   - Literal type usage
   - TypedDict and NamedTuple analysis

4. **Integration Features**
   - Git blame integration to identify contributors of unhinted code
   - Historical trend tracking (type hint coverage over time)
   - Comparison between branches/commits
   - Integration with pre-commit hooks

5. **Performance Optimizations**
   - Parallel file processing for large codebases
   - Incremental analysis (only changed files)
   - Caching of mypy results

6. **Enhanced Reporting**
   - HTML report generation with interactive charts
   - Markdown report for easy GitHub integration
   - Diff reports showing improvement/regression
   - Per-developer statistics

### Contributing

If you'd like to improve the type hint analyzer:

1. The main implementation is in `type-analyzer.py`
2. The CSV generator is in `gen-csv.py`
3. Both scripts follow PyThaiNLP coding standards
4. Run Ruff before submitting changes: `ruff check build_tools/analysis/`
5. Ensure all docstrings are complete and follow reStructuredText format
6. Test changes by running the analyzer on the full repository

For questions or suggestions, please open an issue in the PyThaiNLP repository.

## Understanding variable type annotations

### What should be annotated

According to Python typing best practices and type checking tools like mypy,
type annotations should be added to:

1. **First assignment** of a variable
2. **Variables where type isn't obvious** from the assigned value
3. **Class and instance variables** (on first assignment only)

### What should not be annotated

1. **Reassignments** - Adding type annotations to reassignments causes `no-redef` errors
2. **Dictionary subscript operations** - Cannot annotate `dict[key] = value` operations
3. **Variables with obvious literal types** - Optional, but generally omitted for simple cases

## Future Tools

This directory can be extended with additional analysis tools:

- Code complexity analysis
- Documentation coverage analysis
- API stability analysis
- Dependency analysis
