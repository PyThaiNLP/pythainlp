# Type Hint Analysis Data Files

This directory contains detailed data files from the type hint coverage
analysis.

## Files

### type_hint_analysis.json

Raw JSON data from the analysis containing all detailed information about
functions, methods, and statistics.

### submodule_summary.csv

Summary statistics for each submodule showing:

- Total number of functions/methods
- Count with complete type hints
- Count with incomplete type hints
- Count without type hints
- Percentage with complete type hints
- Number of mypy errors detected

### functions_no_hints.csv

Complete list of functions and methods **without any type hints**, including:

- Function Name (fully qualified)
- Submodule
- Scope (public/private)
- Priority (high/medium/low)
- Number of internal references
- Test Suite (core/compact/extra/noauto/unknown)
- File path and line number

### functions_incomplete_hints.csv

Complete list of functions and methods **with incomplete type hints**,
including:

- Function Name (fully qualified)
- Submodule
- Scope (public/private)
- Priority (high/medium/low)
- Parameters with hints (e.g., "2/3" means 2 out of 3 parameters have type
  hints)
- Has Return hint (True/False)
- Number of internal references
- Test Suite (core/compact/extra/noauto/unknown)
- File path and line number

## Usage

These files can be:

- Opened in spreadsheet applications (Excel, Google Sheets, LibreOffice Calc)
- Imported into databases for analysis
- Processed with command-line tools (`csvkit`, `pandas`, etc.)
- Used to track progress on improving type hint coverage

## Filtering Examples

### Find high-priority public functions without hints

```bash
csvgrep -c Priority -m "high" functions_no_hints.csv | csvgrep -c Scope -m "public"
```

### Show functions in a specific submodule

```bash
csvgrep -c Submodule -m "transliterate" functions_no_hints.csv
```

### Sort by number of references

```bash
csvsort -c References -r functions_no_hints.csv
```

## Related Files

- `../../../TYPE_HINT_ANALYSIS.md` - Comprehensive analysis report
- `../type_hint_analyzer.py` - Main analyzer script
- `../generate_csv.py` - CSV generator script

## Updating the Analysis

To regenerate this analysis:

```bash
# Navigate to the analysis directory
cd build_tools/analysis

# Run the analyzer
python3 type_hint_analyzer.py

# Generate CSV files
python3 generate_csv.py
```
