# Test Coverage Improvements

## Summary

This document summarizes the test coverage improvements made to the PyThaiNLP project based on the analysis of the Coveralls test coverage report.

## Modules with Improved Coverage

### Core Tests (test_*.py)

#### 1. `pythainlp.tools.core` Module
**File**: `tests/core/test_tools.py`

Added comprehensive tests for:
- `warn_deprecation()` - Deprecation warning function
  - Test basic deprecation warning
  - Test with replacement function
  - Test with version information
  - Test with all parameters combined
- `safe_print()` - Safe printing with UnicodeEncodeError handling
  - Test normal printing
  - Test with Unicode characters
  - Test with empty strings
  - Test with special characters

**New Test Count**: 2 test methods covering 8+ test cases

#### 2. `pythainlp.util.encoding` Module
**File**: `tests/core/test_util.py`

Enhanced existing tests with edge cases for:
- `tis620_to_utf8()` - TIS-620 to UTF-8 conversion
  - Additional Thai text conversions
  - Empty string handling
- `to_idna()` - IDNA encoding for internationalized domain names
  - Multiple Thai domain examples
  - ASCII domain handling (unchanged)

**Enhanced Test Count**: 2 test methods with 4+ additional test cases

#### 3. `pythainlp.ancient` Module
**File**: `tests/core/test_ancient.py`

Enhanced existing tests with edge cases for:
- `aksonhan_to_current()` - AksonHan to current Thai conversion
  - Empty string handling
  - Single character handling
  - Two character strings
- `convert_currency()` - Ancient Thai currency conversion
  - All supported currency units
  - Zero value handling
  - Fractional value handling
  - Invalid unit error handling

**Enhanced Test Count**: 2 test methods with 7+ additional test cases

#### 4. Utility Functions Edge Cases
**File**: `tests/core/test_util.py`

Enhanced existing tests for:
- `longest_common_subsequence()` - LCS algorithm
  - Empty strings (both, one, other)
  - Single character matches and non-matches
  - Identical strings
  - No common characters
  - Thai text examples
- `emoji_to_thai()` - Emoji to Thai text conversion
  - Empty strings
  - Text with no emoji
  - Thai text with no emoji
- `collate()` - Thai text collation
  - Mixed Thai and numbers
  - Strings with spaces

**Enhanced Test Count**: 3 test methods with 12+ additional test cases

### Compact Tests (testc_*.py)

#### 5. `pythainlp.tools.misspell` Module
**File**: `tests/compact/testc_tools.py`

Added comprehensive tests for helper functions:
- `search_location_of_character()` - Find character location on keyboard
  - Thai character handling
  - English character handling
  - Shifted character handling
  - Number handling
  - Characters not on keyboard (returns None)
  - Empty string handling
- `find_misspell_candidates()` - Find possible misspelling candidates
  - Thai character candidates
  - English character candidates
  - Characters not on keyboard
  - Validation that candidates are strings

**New Test Count**: 2 test methods covering 12+ test cases

## Coverage Statistics

### Before
Based on Coveralls report analysis, several modules had no or minimal test coverage:
- `pythainlp.tools.core` - No tests for `warn_deprecation()` and `safe_print()`
- `pythainlp.tools.misspell` helper functions - Only the main `misspell()` function was tested
- Edge cases in utility functions - Missing edge case coverage for empty inputs, special characters, etc.
- `pythainlp.ancient` module - Basic tests only, missing edge cases

### After
- **Core module tests added**: 4 new test methods, 27+ new test cases
- **Compact module tests added**: 2 new test methods, 12+ new test cases
- **Total new test coverage**: 6 test methods, 39+ test cases

## Test Categories

All tests follow the established test categorization:

1. **Core Tests** (`test_*.py`)
   - No external dependencies beyond standard library
   - Test case class suffix: `TestCase`
   - Run with: `python -m unittest tests.core`

2. **Compact Tests** (`testc_*.py`)
   - Depend on: PyYAML, nlpo3, numpy, pyicu, python-crfsuite, requests
   - Test case class suffix: `TestCaseC`
   - Run with: `python -m unittest tests.compact`

## Files Modified

1. `tests/core/test_tools.py` - Added 2 new test methods
2. `tests/core/test_ancient.py` - Enhanced with edge cases
3. `tests/core/test_util.py` - Enhanced 5 test methods with edge cases
4. `tests/compact/testc_tools.py` - Added 2 new test methods

## Running the New Tests

```bash
# Run all modified core tests
python -m unittest tests.core.test_tools tests.core.test_ancient tests.core.test_util -v

# Run compact tests
python -m unittest tests.compact.testc_tools -v

# Run specific new test methods
python -m unittest tests.core.test_tools.ToolsTestCase.test_warn_deprecation -v
python -m unittest tests.core.test_tools.ToolsTestCase.test_safe_print -v
python -m unittest tests.compact.testc_tools.MisspellTestCaseC.test_search_location_of_character -v
python -m unittest tests.compact.testc_tools.MisspellTestCaseC.test_find_misspell_candidates -v
```

## Recommendations for Further Testing

Based on the analysis, these modules still need more test coverage:

### High Priority (Core functionality, no tests)
1. `pythainlp.chat.core` - ChatBot model loading and chat functions
2. `pythainlp.coref._fastcoref` - Coreference resolution
3. `pythainlp.benchmarks` - Benchmarking utilities

### Medium Priority (Utility functions, minimal tests)
1. `pythainlp.util.keyboard` - More edge cases for keyboard distance
2. `pythainlp.util.thai_lunar_date` - Date conversion functions
3. `pythainlp.util.morse` - More edge cases for encoding/decoding

### Low Priority (Advanced features, require heavy dependencies)
1. Specialized tokenizers (ssg, deepcut, etcc, etc.)
2. Parser modules (spacy_thai_engine, transformers_ud, etc.)
3. Model-based taggers and classifiers

## Notes

- All new tests follow the project's test categorization system
- Tests are written to pass existing linting and formatting requirements
- Edge cases focus on empty inputs, boundary conditions, and error handling
- Tests maintain consistency with existing test patterns in the codebase
