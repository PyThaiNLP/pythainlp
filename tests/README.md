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

## Test matrix for CI

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

The noauto (no-automated) test suite contains tests for functionalities
that require heavy dependencies which are not feasible to run in automated
CI/CD pipelines. These tests are organized into specialized suites based
on their dependency requirements.

### Why separate noauto test suites?

Different ML/AI frameworks often have conflicting version requirements for
their dependencies. For example:
- PyTorch and TensorFlow may require different versions of numpy or protobuf
- Large frameworks take significant time to install (~1-3 GB each)
- Some packages require Cython compilation or system libraries

By separating tests by dependency group, we can:
- Test each framework independently without conflicts
- Optimize CI/CD resources by running only relevant test groups
- Make it easier for developers to test specific functionality

### Noauto test suites

#### Umbrella suite: tests.noauto

- Run `unittest tests.noauto`
- Includes all modular noauto test suites
- Use this for comprehensive testing when all dependencies are available
- Test case class suffix: `TestCaseN`

#### Modular suites by dependency:

**PyTorch-based: tests.noauto_torch**

- Run `unittest tests.noauto_torch`
  - Need dependencies from `pip install "pythainlp[noauto-torch]"`
- Tests requiring PyTorch and its ecosystem:
  - torch, transformers (PyTorch backend)
  - attacut, thai-nner, wtpsplit, tltk
- Tests: spell correction (wanchanberta), NER/POS tagging (transformers-based),
  tokenization (attacut), subword tokenization (phayathai, wangchanberta),
  sentence tokenization (wtp)
- Dependencies: ~2-3 GB
- Test case class suffix: `TestCaseN`

**TensorFlow-based: tests.noauto_tensorflow**

- Run `unittest tests.noauto_tensorflow`
  - Need dependencies from `pip install "pythainlp[noauto-tensorflow]"`
- Tests requiring TensorFlow:
  - deepcut tokenizer
- Dependencies: ~1-2 GB
- Note: May conflict with PyTorch dependencies
- Test case class suffix: `TestCaseN`

**ONNX Runtime-based: tests.noauto_onnx**

- Run `unittest tests.noauto_onnx`
  - Need dependencies from `pip install "pythainlp[noauto-onnx]"`
- Tests requiring ONNX Runtime:
  - oskut, sefr_cut tokenizers
- Dependencies: ~200-500 MB
- Test case class suffix: `TestCaseN`

**Cython-compiled: tests.noauto_cython**

- Run `unittest tests.noauto_cython`
  - Need dependencies from `pip install "pythainlp[noauto-cython]"`
- Tests requiring Cython-compiled packages:
  - phunspell spell checker
- Requires: Cython, C compiler, system libraries (hunspell)
- Platform-specific build requirements
- Test case class suffix: `TestCaseN`

**Network-dependent: tests.noauto_network**

- Run `unittest tests.noauto_network`
  - Need dependencies from `pip install "pythainlp[noauto-network]"`
- Tests requiring network access:
  - HuggingFace Hub model downloads
  - External API calls
- Requires: Internet connection, may involve large downloads
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

## Corpus integrity tests (corpus_integrity/)

A separate test suite that verifies the integrity, format, and parseability
of corpus files in PyThaiNLP. These tests are separate from regular unit tests
because they test actual file loading and parsing (not mocked) and downloadable
corpus tests require network access.

For detailed information about corpus integrity tests, see:
[tests/corpus_integrity/README.md](corpus_integrity/README.md)

The corpus integrity tests are triggered automatically via GitHub Actions
when changes are made to `pythainlp/corpus/**` or `tests/corpus_integrity/**`.

**Run corpus integrity tests:**
```shell
python -m unittest tests.corpus_integrity
```
