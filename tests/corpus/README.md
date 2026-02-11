---
SPDX-FileCopyrightText: 2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: Apache-2.0
---

# Corpus test

This directory contains tests that verify the integrity, format,
parseability, and catalog functionality of corpus in PyThaiNLP.

## Purpose

These tests are separate from regular unit tests because:

1. They test actual file loading and parsing (not mocked)
2. Downloadable corpus tests require network access and can be slow
3. They verify corpus format and structure
4. They test corpus catalog download and query functionality
5. They should only run when corpus files or corpus code changes

## Test categories

### Corpus catalog tests (`test_catalog.py`)

Tests corpus catalog functionality:

- Catalog download from remote server
- Catalog URL and path validation
- Catalog JSON structure verification
- Querying specific corpus details
- Version information validation

### Built-in corpus tests (`test_builtin_corpus.py`)

Tests corpus files that are included in the package:

- Text word lists (negations, stopwords, syllables, words, etc.)
- CSV files (provinces)
- Frequency data (TNC, TTC)
- Name lists (family names, person names)

### Downloadable corpus tests (`test_downloadable_corpus.py`)

Tests corpus files that need to be downloaded:

- OSCAR word frequencies (96MB)
- TNC bigram/trigram frequencies (41MB + 145MB)

This test will take longer time than others due to
size of the downloads.

## Running tests

Run all corpus tests:

```bash
python -m unittest discover -s tests/corpus -v
```

Run only catalog tests:

```bash
python -m unittest tests.corpus.test_catalog -v
```

Run only built-in corpus tests:

```bash
python -m unittest tests.corpus.test_builtin_corpus -v
```

Run only downloadable corpus tests:

```bash
python -m unittest tests.corpus.test_downloadable_corpus -v
```

## CI integration

The corpus test runs automatically via
GitHub Actions workflow (`.github/workflows/corpus.yml`) when:

- Changes are made to `pythainlp/corpus/**`
- Changes are made to `tests/corpus/**`
- The workflow file itself is modified

## What is tested

Each test verifies:

1. **Loadability**: File can be loaded without errors
2. **Type correctness**: Returns expected data type
   (frozenset, list, dict)
3. **Non-empty**: Contains actual data
4. **Format validity**: Data structure matches expected format
5. **Content validity**: Contains expected content
   (e.g., Thai characters)
6. **Catalog functionality**: Catalog can be downloaded
   and queried correctly

## Adding new tests

When adding a new corpus file or function to `pythainlp.corpus`:

1. Add a test to `test_builtin_corpus.py` if it's included in the package
2. Add a test to `test_downloadable_corpus.py` if it requires download
3. Add a test to `test_catalog.py` if it involves catalog operations
4. Verify the test catches format errors by temporarily breaking the corpus

## Relationship to unit tests

- **Unit tests** (`tests/core/test_corpus.py`):
  Use mocks for speed, test code logic
- **Corpus test** (this directory):
  Use real data, test file integrity and catalog

Both test suites are important and complementary.
