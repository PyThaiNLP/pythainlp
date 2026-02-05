# Test suites and execution

To run a test suite, run:

```shell
unittest tests.<test_suite_name>
```

This command will run a default set of test suites:

```shell
unittest tests
```

The default test suite includes all test suites listed in `tests/__init__.py` file.
Currently, it includes `tests.core` and `tests.compact`.

To optimize CI/CD resource utilization and manage dependency overhead,
tests are categorized into four tiers based on their resource
requirements and complexity: "core", "compact", "extra", and "noauto".

## Adding a test case to a test suite

To add a test case to a test suite,
add it to `tests_packages` list in `__init__.py`
inside that test suite's directory.

## Test matrix

The following table outlines the automated test coverage across
supported Python versions and operating systems:

| Python         | Ubuntu  | Windows | macOS |
| -------------- | ------- | ------- | ----- |
| 3.14 (Latest)  | O+C     | O       | O     |
| 3.13           | O+C+X   | O+C     | O+C   |
| 3.12           | O       |         |       |
| 3.11           | O       |         |       |
| 3.10           | O       |         |       |
| 3.9 (Earliest) | O+C     | O+C     | O+C   |

The CI/CD test workflow is at
<https://github.com/PyThaiNLP/pythainlp/blob/dev/.github/workflows/unittest.yml>.

## Core tests (test_*.py)

- Run `unittest tests.core`
- Focus on core functionalities.
- Do not rely on external dependencies beyond the standard library.
- Tested on all supported operating systems and all active Python versions.
- Test case class suffix: `TestCase`

## Compact tests (testc_*.py)

- Run `unittest tests.compact`
  - Need dependencies from `pip install "pythainlp[compact]"`
- Test a limited set of functionalities that rely on a stable
  and small set of dependencies.
- These dependencies are `PyYAML`, `nlpo3`, `numpy`, `pyicu`,
  `python-crfsuite`, and `requests`.
- Tested on:
  - All OSes: earliest and second-latest supported Python versions
  - Ubuntu: additionally tested on the latest version
- Test case class suffix: `TestCaseC`

## Extra tests (testx_*.py)

- Run `unittest tests.extra`
  - Need dependencies from `pip install "pythainlp[compact,extra]"`
- Test more functionalities that rely on larger set of dependencies
  or one that require more time or computation.
- Only tested on Ubuntu using the second-latest Python version.
- Test case class suffix: `TestCaseX`

## Noauto tests (testn_*.py)

- These dependencies might include huge libraries like `tensorflow`.
- Due to dependency complexities, these functionalities may not be tested
  in the CI/CD pipeline.
  - In the future, we might create a separate
    step or workflow to run this test suite.
    It will be triggered manually.
    We may also need to group test cases by
    a non-conflicting set of dependencies.
- Test case class suffix: `TestCaseN`

## Robustness tests (test_robustness.py)

A comprehensive test suite within core tests that tests edge cases important
for real-world usage:

- Empty strings and various whitespace handling (spaces, tabs, Unicode spaces)
- Special characters from encoding issues, BOM, terminal copy/paste
- Truncated/malformed Unicode and surrogate pairs
- Emoji and modern Unicode sequences (ZWJ, modifiers, flags)
- Control and hidden/invisible characters (zero-width, control chars)
- Thai-specific edge cases with combining characters and mixed scripts
- Multi-engine robustness testing across all core tokenization engines
- Very long strings that can cause performance issues (issue #893)
