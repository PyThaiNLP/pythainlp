# Type Hint Analysis Data Files

This directory contains detailed data files from the type hint coverage analysis.

## Files

### submodule_summary.csv
Summary statistics for each submodule showing:
- Total number of functions/methods
- Count with complete type hints
- Count with incomplete type hints
- Count without type hints
- Percentage with complete type hints

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
Complete list of functions and methods **with incomplete type hints**, including:
- Function Name (fully qualified)
- Submodule
- Scope (public/private)
- Priority (high/medium/low)
- Parameters with hints (e.g., "2/3" means 2 out of 3 parameters have type hints)
- Has Return hint (True/False)
- Number of internal references
- Test Suite (core/compact/extra/noauto/unknown)
- File path and line number

## Usage

These CSV files can be:
- Opened in spreadsheet applications (Excel, Google Sheets, LibreOffice Calc)
- Imported into databases for analysis
- Processed with command-line tools (`csvkit`, `pandas`, etc.)
- Used to track progress on improving type hint coverage

## Filtering Examples

### Find high-priority public functions without hints:
```bash
csvgrep -c Priority -m "high" functions_no_hints.csv | csvgrep -c Scope -m "public"
```

### Show functions in a specific submodule:
```bash
csvgrep -c Submodule -m "transliterate" functions_no_hints.csv
```

### Sort by number of references:
```bash
csvsort -c References -r functions_no_hints.csv
```

## Related Files

- `../../TYPE_HINT_ANALYSIS.md` - Comprehensive analysis report in markdown format
- `../../build_tools/analysis/type_hint_analyzer.py` - Main analyzer script
- `../../build_tools/analysis/generate_csv.py` - CSV generator script

## Updating the Analysis

To regenerate this analysis, run from the repository root:
```bash
python3 build_tools/analysis/type_hint_analyzer.py
python3 build_tools/analysis/generate_csv.py
cp /tmp/*.csv docs/type_hint_analysis/
```
