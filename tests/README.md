# Test cases

Tests are categorized into three groups: core, compact, and extra.

## Core Tests (test_*.py)

- Run `unittest tests.core`
- Focus on core functionalities.
- Do not rely on external dependencies beyond the standard library,
  except for `requests` which is used for corpus downloading.
- Test with all officially supported Python versions
  (currently 3.9, 3.10, 3.11, 3.12, and 3.13).

### Robustness Tests (test_robustness.py)

A comprehensive test suite within core tests that tests edge cases important
for real-world usage:

- Empty strings and various whitespace handling (spaces, tabs, unicode spaces)
- Special characters from encoding issues, BOM, terminal copy/paste
- Truncated/malformed Unicode and surrogate pairs
- Emoji and modern Unicode sequences (ZWJ, modifiers, flags)
- Control and hidden/invisible characters (zero-width, control chars)
- Thai-specific edge cases with combining characters and mixed scripts
- Multi-engine robustness testing across all core tokenization engines
- Very long strings that can cause performance issues (issue #893)

## Compact Tests (testc_*.py)

- Run `unittest tests.compact`
- Test a limited set of functionalities that rely on a stable and small subset
  of optional dependencies specified in `requirements.txt`.
- These dependencies are `PyYAML`, `nlpo3`, `numpy`, `pyicu`,
  `python-crfsuite`, and `requests`.
- Test with the latest two stable Python versions.

## Extra Tests (testx_*.py)

- Run `unittest tests.extra`
- Explore functionalities that rely on optional dependencies specified in the
  `project.optional-dependencies` section of `pyproject.toml`.
- These dependencies might include libraries like `gensim`, `tltk`, or `torch`.
- Due to dependency complexities, these functionalities are not part of the
  automated test suite and will not be tested in the CI/CD pipeline.

## Default Test Suite

The default test suite, triggered by the `unittest tests` command, encompasses
all test cases within the `tests.core` and `tests.compact` packages.
This suite is defined within the `__init__.py` file in this directory.
