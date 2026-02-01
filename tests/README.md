# Test cases

The default test suite, triggered by the `unittest tests` command, encompasses
all test cases within the `tests.core` and `tests.compact` packages.
This suite is defined within the `__init__.py` file in this directory.

Tests are categorized into three groups: core, compact, and extra.

## Core tests (test_*.py)

- Run `unittest tests.core`
- Focus on core functionalities.
- Do not rely on external dependencies beyond the standard library.
- Test with all officially supported Python versions
  (currently 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14).

## Compact tests (testc_*.py)

- Run `unittest tests.compact`
- Test a limited set of functionalities that rely on a stable and small subset
  of optional dependencies specified in `pyproject.toml`.
- These dependencies are `PyYAML`, `nlpo3`, `numpy`, `pyicu`,
  `python-crfsuite`, and `requests`.
- Test with the latest two stable Python versions.

## Extra tests (testx_*.py)

- Run `unittest tests.extra`
- Explore functionalities that rely on optional dependencies specified in the
  `project.optional-dependencies` section of `pyproject.toml`.

## Noauto tests (testn_*.py)

- These dependencies might include huge libraries like `tensorflow`.
- Due to dependency complexities, these functionalities may not be tested
  in the CI/CD pipeline.

## Robustness tests (test_robustness.py)

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
