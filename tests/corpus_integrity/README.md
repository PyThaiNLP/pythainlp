# Corpus Integrity Tests

This directory contains tests that verify the integrity, format, and parseability of corpus files in PyThaiNLP.

## Purpose

These tests are separate from regular unit tests because:
1. They test actual file loading and parsing (not mocked)
2. Downloadable corpus tests require network access and can be slow
3. They verify corpus data format and structure
4. They should only run when corpus files or corpus code changes

## Test Categories

### Built-in Corpus Tests (`test_builtin_corpus.py`)

Tests corpus files that are included in the package:
- Text word lists (negations, stopwords, syllables, words, etc.)
- CSV files (provinces)
- Frequency data (TNC, TTC)
- Name lists (family names, person names)

**Run time:** < 1 second

### Downloadable Corpus Tests (`test_downloadable_corpus.py`)

Tests corpus files that need to be downloaded:
- OSCAR word frequencies (96MB)
- TNC bigram/trigram frequencies (41MB + 145MB)

**Run time:** ~17 seconds (includes download time)

## Running Tests

### Run all corpus integrity tests:
```bash
python -m unittest discover -s tests/corpus_integrity -v
```

### Run only built-in corpus tests:
```bash
python -m unittest tests.corpus_integrity.test_builtin_corpus -v
```

### Run only downloadable corpus tests:
```bash
python -m unittest tests.corpus_integrity.test_downloadable_corpus -v
```

## CI Integration

The corpus integrity tests run automatically via GitHub Actions workflow (`.github/workflows/corpus-integrity.yml`) when:
- Changes are made to `pythainlp/corpus/**`
- Changes are made to `tests/corpus_integrity/**`
- The workflow file itself is modified

## What is Tested

Each test verifies:
1. **Loadability**: File can be loaded without errors
2. **Type correctness**: Returns expected data type (frozenset, list, dict)
3. **Non-empty**: Contains actual data
4. **Format validity**: Data structure matches expected format
5. **Content validity**: Contains expected content (e.g., Thai characters)

## Adding New Tests

When adding a new corpus file or function to `pythainlp.corpus`:
1. Add a test to `test_builtin_corpus.py` if it's included in the package
2. Add a test to `test_downloadable_corpus.py` if it requires download
3. Verify the test catches format errors by temporarily breaking the corpus

## Relationship to Unit Tests

- **Unit tests** (`tests/core/test_corpus.py`): Use mocks for speed, test code logic
- **Corpus integrity tests** (this directory): Use real data, test file integrity

Both test suites are important and complementary.
