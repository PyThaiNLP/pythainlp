# Type Hint Coverage Analysis for PyThaiNLP

**Analysis Date:** 2026-02-03

This document provides a comprehensive analysis of type hint coverage
across the PyThaiNLP codebase.

## Executive Summary

The PyThaiNLP codebase demonstrates **strong type hint coverage** with
82.22% of functions and methods having complete type hints.

- **Total functions/methods analyzed:** 720
- **Complete type hints:** 592 (82.22%)
- **Incomplete type hints:** 56 (7.78%)
- **No type hints:** 72 (10.00%)

## Overall Statistics

| Category | Count | Percentage |
| -------- | ----- | ---------- |
| Complete type hints | 592 | 82.22% |
| Incomplete type hints | 56 | 7.78% |
| No type hints | 72 | 10.00% |
| **Total** | **720** | **100.00%** |

## Breakdown by Submodule

### Excellent Coverage (95%+)

| Submodule | Total | Complete | Incomplete | None | % Complete | Mypy |
| --------- | ----- | -------- | ---------- | ---- | ---------- | ---- |
| **cli** | 21 | 21 | 0 | 0 | 100.00% | 6 |
| **lm** | 2 | 2 | 0 | 0 | 100.00% | 6 |
| **morpheme** | 2 | 2 | 0 | 0 | 100.00% | 6 |
| **parse** | 9 | 9 | 0 | 0 | 100.00% | 6 |
| **tokenizeicu** | 3 | 3 | 0 | 0 | 100.00% | - |
| **tools** | 9 | 9 | 0 | 0 | 100.00% | 6 |
| **transliterateicu** | 1 | 1 | 0 | 0 | 100.00% | - |
| **word_vector** | 7 | 7 | 0 | 0 | 100.00% | 8 |
| **ancient** | 2 | 2 | 0 | 0 | 100.00% | 6 |
| **corpus** | 70 | 68 | 1 | 1 | 97.14% | 6 |
| **tag** | 68 | 66 | 2 | 0 | 97.06% | 7 |
| **soundex** | 27 | 26 | 0 | 1 | 96.30% | 6 |
| **spell** | 43 | 41 | 2 | 0 | 95.35% | 6 |

### Good Coverage (80-94%)

| Submodule | Total | Complete | Incomplete | None | % Complete | Mypy |
| --------- | ----- | -------- | ---------- | ---- | ---------- | ---- |
| **util** | 109 | 103 | 4 | 2 | 94.50% | 6 |
| **phayathaibert** | 19 | 17 | 0 | 2 | 89.47% | 6 |
| **benchmarks** | 8 | 7 | 1 | 0 | 87.50% | 6 |
| **tokenize** | 73 | 62 | 3 | 8 | 84.93% | 6 |
| **translate** | 44 | 37 | 5 | 2 | 84.09% | 6 |

### Moderate Coverage (50-79%)

| Submodule | Total | Complete | Incomplete | None | % Complete | Mypy |
| --------- | ----- | -------- | ---------- | ---- | ---------- | ---- |
| **khavee** | 9 | 7 | 0 | 2 | 77.78% | 6 |
| **summarize** | 17 | 12 | 5 | 0 | 70.59% | 9 |
| **ulmfit** | 25 | 17 | 4 | 4 | 68.00% | 6 |
| **augment** | 29 | 18 | 4 | 7 | 62.07% | 6 |
| **generate** | 15 | 8 | 6 | 1 | 53.33% | 6 |
| **wsd** | 4 | 2 | 2 | 0 | 50.00% | 6 |

### Needs Improvement (<50%)

| Submodule | Total | Complete | Incomplete | None | % Complete | Mypy |
| --------- | ----- | -------- | ---------- | ---- | ---------- | ---- |
| **transliterate** | 75 | 36 | 9 | 30 | 48.00% | 6 |
| **wangchanberta** | 9 | 4 | 1 | 4 | 44.44% | 6 |
| **coref** | 5 | 2 | 2 | 1 | 40.00% | 6 |
| **chat** | 4 | 1 | 1 | 2 | 25.00% | 6 |
| **classify** | 5 | 1 | 3 | 1 | 20.00% | 6 |
| **el** | 5 | 1 | 1 | 3 | 20.00% | 6 |
| **main** | 1 | 0 | 0 | 1 | 0.00% | 0 |

## Priority Analysis

Functions and methods are categorized by priority based on:

- **Scope:** Public vs. private
- **Internal references:** How frequently they're used within the package
- **Test coverage:** Which test suite they belong to (core, compact, extra,
  noauto)

### High Priority Items

**Criteria:** Public functions with >10 internal references in core/compact
test suites

**Finding:** No functions without type hints fall into this category,
indicating that the most critical, widely-used public APIs are well-covered.

### Medium Priority Items

**Criteria:** Public functions with 3-10 references

**Functions without type hints (51 total):**

Top items include:

- `pythainlp.corpus.util.tokenize` (991 references)
- `pythainlp.classify.param_free.GzipModel.train` (164 references)
- Various `__init__` methods across multiple classes (113 references each)

**Functions with incomplete type hints (43 total):**

Top items include:

- `pythainlp.tokenize.nercut.segment` (2/3 params hinted)
- `pythainlp.classify.param_free.GzipModel.load` (missing return type)
- Various `__init__` methods missing return type hints

### Low Priority Items

**Criteria:** Private functions or rarely referenced functions

- **21 functions** without type hints
- **13 functions** with incomplete type hints

## Test Suite Coverage

Functions are mapped to test suites based on the test categorization:

- **core:** Core functionality tests (no external dependencies)
- **compact:** Tests with stable, small dependencies
- **extra:** Tests with larger dependencies
- **noauto:** Tests not run in CI/CD (e.g., TensorFlow dependencies)
- **unknown:** Functions not clearly mapped to a test suite

Most functions requiring type hint improvements are either in "unknown"
test suite category or are tested indirectly.

## Recommendations

### Immediate Actions (High Priority)

1. **Complete coverage for widely-used public APIs**
   - ✅ Already achieved - no high-priority items without type hints

### Short-term Improvements (Medium Priority)

1. **transliterate submodule** (48.00% coverage)
   - Focus on 30 functions without type hints
   - Address 9 functions with incomplete hints

2. **classify submodule** (20.00% coverage)
   - Add type hints to 3 incomplete functions
   - Add type hints to 1 function without hints

3. **el (entity linking) submodule** (20.00% coverage)
   - Add type hints to 3 functions without hints
   - Complete 1 function with incomplete hints

4. **chat submodule** (25.00% coverage)
   - Add type hints to 2 functions without hints
   - Complete 1 function with incomplete hints

5. **wangchanberta submodule** (44.44% coverage)
   - Add type hints to 4 functions without hints
   - Complete 1 function with incomplete hints

6. **Add return type hints to `__init__` methods**
   - Many class `__init__` methods are missing `-> None` return type
   - This is a quick win that significantly improves completeness

### Long-term Goals

1. **Achieve 95%+ coverage across all submodules**
2. **Maintain type hint standards for new code**
3. **Gradually improve coverage in legacy code during maintenance**

## Detailed Results

Full analysis results with file locations and line numbers are available in:

- **JSON format:** `/tmp/type_hint_analysis.json`
- **Text report:** Contains full listings of all functions by priority

## Analysis Methodology

This analysis was performed using a custom AST-based analyzer that:

1. Scans all Python files in the repository
2. Parses function and method definitions using Python's `ast` module
3. Checks for type hints on parameters and return values
4. Categorizes functions by:
   - Completeness (complete/incomplete/none)
   - Scope (public/private)
   - Internal reference count
   - Test suite mapping
5. Assigns priority based on the above factors
6. Runs mypy on each submodule to count type-related errors

**Notes:**

- Classes themselves are not scored (only their methods)
- `self` and `cls` parameters are excluded from type hint requirements
- Functions with no parameters and no return type hint are marked as "none"
- Functions with all parameters typed and return type are marked as
  "complete"
- Everything else is marked as "incomplete"

## Conclusion

PyThaiNLP demonstrates **strong type hint adoption** with 82.22% complete
coverage. The codebase has excellent coverage in core modules (cli, corpus,
tag, spell) and good coverage in most other areas.

The main areas for improvement are specialized modules like `transliterate`,
`classify`, `el`, and `chat`, which represent opportunities for enhancing
type safety and developer experience.

---

This report was automatically generated on 2026-02-03.
