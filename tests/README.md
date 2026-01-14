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

A special test suite within core tests that focuses on testing
the robustness, reliability, and security of PyThaiNLP functions
using edge cases from the Big List of Naughty Strings (BLNS).

- Tests functions with unusual inputs like empty strings, null values,
  special characters, unicode edge cases, and potential injection strings.
- Ensures functions handle edge cases gracefully without crashing or
  executing unintended code.
- Gradually expanding to cover more categories from BLNS.
- More info: https://github.com/minimaxir/big-list-of-naughty-strings

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
  `extras` section of `setup.py`.
- These dependencies might include libraries like `gensim`, `tltk`, or `torch`.
- Due to dependency complexities, these functionalities are not part of the
  automated test suite and will not be tested in the CI/CD pipeline.

## Default Test Suite

The default test suite, triggered by the `unittest tests` command, encompasses
all test cases within the `tests.core` and `tests.compact` packages.
This suite is defined within the `__init__.py` file in this directory.
