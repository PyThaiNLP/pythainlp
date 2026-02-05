# PyThaiNLP Fuzz Testing

This directory contains fuzz testing infrastructure using
[ClusterFuzzLite](https://google.github.io/clusterfuzzlite/) and [Atheris](https://github.com/google/atheris).

## Overview

Fuzz testing helps discover edge cases, crashes, and potential security vulnerabilities by feeding random inputs to functions. This setup uses:

- **ClusterFuzzLite**: Google's continuous fuzzing solution for GitHub projects
- **Atheris**: Coverage-guided Python fuzzing engine
- **AddressSanitizer**: Memory safety checks

## Directory Structure

```
fuzz/
├── Dockerfile                 # Docker image for ClusterFuzzLite fuzzing
├── build.sh                   # Build script for compiling fuzzers
├── fuzz_tokenize.py           # Fuzzer for word_tokenize()
├── fuzz_util_normalize.py     # Fuzzer for normalize()
└── README.md                  # This file
```

## Current Fuzzing Targets

### 1. `fuzz_tokenize.py`
Tests `pythainlp.tokenize.word_tokenize()` with random Unicode input to ensure:
- No crashes on malformed input
- Proper handling of edge cases
- Memory safety

### 2. `fuzz_util_normalize.py`
Tests `pythainlp.util.normalize()` with random Unicode input to ensure:
- No crashes on malformed input
- Proper string normalization
- Type safety

## Local Testing

To test fuzzers locally:

```bash
# Install atheris
pip install atheris

# Run a specific fuzzer for 60 seconds
python fuzz/fuzz_tokenize.py -max_total_time=60

# Run with specific corpus directory
python fuzz/fuzz_tokenize.py corpus_dir/ -max_total_time=60
```

## CI/CD Integration

Fuzzing runs automatically via GitHub Actions:
- On pull requests to `dev` branch (focuses on code changes)
- On push to `dev` branch
- Daily at 06:00 UTC (full fuzzing run)

Configuration: `.github/workflows/clusterfuzzlite.yml`

## Adding New Fuzzers

To add a new fuzzing target:

1. Create a new file `fuzz/fuzz_<module_name>.py`:

```python
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileType: SOURCE
"""Fuzzing harness for pythainlp.<module>.<function>()"""

import sys
import atheris
import pythainlp.<module>


def TestOneInput(data: bytes) -> None:
    """Fuzz target for <function>."""
    fdp = atheris.FuzzedDataProvider(data)
    
    try:
        # Generate test input
        text = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())
        
        # Call target function
        result = pythainlp.<module>.<function>(text)
        
        # Validate output
        assert isinstance(result, <expected_type>)
        
    except (ValueError, TypeError, UnicodeDecodeError):
        # Expected exceptions
        pass


def main() -> None:
    """Entry point for the fuzzer."""
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
```

2. Ensure the new fuzzer file name follows the ``fuzz_*.py`` pattern so it can be discovered by ``build.sh``, and run ``bash fuzz/build.sh`` locally to verify that your fuzzer is picked up and built.

3. No changes needed to GitHub Actions workflow

## Expansion Plan

Future fuzzing targets to consider:

### High Priority
- **spell/** - Spelling correction functions
- **soundex/** - Phonetic encoding functions
- **transliterate/** - Romanization functions

### Medium Priority
- **corpus/** - Data loading and corpus functions
- **tag/** - Part-of-speech tagging
- **parse/** - Parsing functions

### Low Priority
- **classify/** - Classification functions
- **generate/** - Text generation functions
- **summarize/** - Summarization functions

## Troubleshooting

### Fuzzer Crashes
If a fuzzer finds a crash:
1. Check the GitHub Actions artifacts for crash reports
2. Reproduce locally: `python fuzz/fuzz_<name>.py <crash_file>`
3. Fix the underlying issue in the target function
4. Re-run fuzzer to verify fix

### Performance Issues
- Adjust fuzzing time in `.github/workflows/clusterfuzzlite.yml`
- Default is 300 seconds (5 minutes) per fuzzer
- For longer sessions, increase the value

### False Positives
- Update the exception handling in the fuzzer
- Add expected exceptions to the `except` block
- Document the reasoning in comments

## Resources

- [ClusterFuzzLite Documentation](https://google.github.io/clusterfuzzlite/)
- [Atheris Documentation](https://github.com/google/atheris)
- [OSS-Fuzz](https://github.com/google/oss-fuzz)
- [libFuzzer Tutorial](https://github.com/google/fuzzing/blob/master/tutorial/libFuzzerTutorial.md)
