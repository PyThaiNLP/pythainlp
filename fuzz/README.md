---
SPDX-FileCopyrightText: 2026-present PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# PyThaiNLP fuzz testing

This directory contains fuzz testing infrastructure using
[ClusterFuzzLite](https://google.github.io/clusterfuzzlite/)
and [Atheris](https://github.com/google/atheris).

## Overview

Fuzz testing helps discover edge cases, crashes, and potential security
vulnerabilities by feeding random inputs to functions. This setup uses:

- **ClusterFuzzLite**: Google's continuous fuzzing solution for GitHub projects
- **Atheris**: Coverage-guided Python fuzzing engine
- **AddressSanitizer**: Memory safety checks

## Directory Structure

```text
.clusterfuzzlite/
├── Dockerfile                 # Docker image for ClusterFuzzLite fuzzing
└── build.sh                   # Build script for ClusterFuzzLite

fuzz/
├── fuzz_tokenize.py           # Fuzzer for word_tokenize()
├── fuzz_util_normalize.py     # Fuzzer for normalize()
└── README.md                  # This file
```

ClusterFuzzLite requires the ``Dockerfile`` and ``build.sh`` at
``.clusterfuzzlite/``. The fuzzer Python files live in ``fuzz/``.

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
   # SPDX-FileType: SOURCE
   # SPDX-License-Identifier: Apache-2.0
   """Fuzzing harness for pythainlp.<module>.<function>()"""

   import sys

   import atheris

   with atheris.instrument_imports():
       import pythainlp.<module>


   def test_one_input(data: bytes) -> None:
      """Fuzz target for <function>.

      :param bytes data: Random input bytes from the fuzzer
      :rtype: None
      """
      fdp = atheris.FuzzedDataProvider(data)

      try:
         # Generate test input
         text = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())

         # Call target function
         result = pythainlp.<module>.<function>(text)

         # Validate output (TypeError propagates as a fuzzer finding)
         if not isinstance(result, <expected_type>):
               raise TypeError(
                  f"Expected <expected_type>, got {type(result)}"
               )

      except ValueError:
         # Expected exceptions from the target function.
         # UnicodeDecodeError is a subclass of ValueError, so this
         # catches both.
         pass


   def main() -> None:
      """Entry point for the fuzzer.

      :rtype: None
      """
      atheris.Setup(sys.argv, test_one_input)
      atheris.Fuzz()


   if __name__ == "__main__":
      main()
   ```

2. Ensure the new fuzzer file name follows the ``fuzz_*.py`` pattern,
   so it can be discovered by ``.clusterfuzzlite/build.sh``,
   and run ``bash .clusterfuzzlite/build.sh`` locally to verify
   that your fuzzer is picked up and built.

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

### Known warnings on first run

**``fatal: 'origin/gh-pages' is not a commit``**

On the very first workflow run after the PR is merged, ClusterFuzzLite
will print:

```
fatal: 'origin/gh-pages' is not a commit and a branch 'gh-pages'
cannot be created from it
Switched to a new branch 'gh-pages'
```

This is expected. The `gh-pages` branch does not exist yet, so
ClusterFuzzLite creates it and pushes an empty commit to bootstrap the
corpus storage. Subsequent runs will not show this message.

**``WARNING: no interesting inputs were found so far``**

If the fuzzer imports are not wrapped in
``atheris.instrument_imports()``, libFuzzer receives no coverage
feedback and prints this warning. All harnesses in this directory
wrap their imports correctly:

```python
with atheris.instrument_imports():
    import pythainlp.<module>
```

Ensure any new fuzzer you add follows the same pattern.

### False Positives

- Update the exception handling in the fuzzer
- Add expected exceptions to the `except` block
- Document the reasoning in comments

## Resources

- [ClusterFuzzLite Documentation](https://google.github.io/clusterfuzzlite/)
- [Atheris Documentation](https://github.com/google/atheris)
- [OSS-Fuzz](https://github.com/google/oss-fuzz)
- [libFuzzer Tutorial](https://github.com/google/fuzzing/blob/master/tutorial/libFuzzerTutorial.md)

## Corpus Storage Best Practices

The fuzzing corpus (test inputs that trigger interesting code paths)
is automatically managed by ClusterFuzzLite
and stored in the `gh-pages` branch.
However, if you need to manually manage corpus
data, follow these best practices:

### 1. Minimize and De-duplicate

Keep only the smallest, most unique set of inputs:

```bash
# Use libFuzzer's merge feature to minimize corpus
python fuzz/fuzz_tokenize.py -merge=1 minimized_corpus/ original_corpus/

# This keeps only inputs that trigger unique code coverage
```

The `-merge=1` flag tells libFuzzer to:

- Remove duplicate inputs that cover the same code paths
- Keep the smallest input for each unique coverage pattern
- Output the minimized corpus to the first directory

### 2. Sanitize the Data

**Never use sensitive production data for fuzzing:**

- ✅ Use synthetic test data
- ✅ Use publicly available sample data
- ✅ Generate random valid inputs
- ❌ Do not use real user data
- ❌ Do not use data containing secrets, passwords, or API keys
- ❌ Do not use data with personally identifiable information (PII)

**Before committing any corpus:**

```bash
# Review corpus files for sensitive data
find corpus/ -type f -exec head -n 5 {} \;

# Check for common patterns
grep -r "password\|api_key\|secret\|token" corpus/
```

### 3. Use Dedicated Storage

**ClusterFuzzLite automatically stores corpus in `gh-pages` branch**,
which is separate from the main codebase.
This is the recommended approach.

**If storing corpus locally or in version control:**

- ❌ Do NOT add corpus to the main branch with `git add fuzz/corpus/`
- ✅ Use a dedicated branch (e.g., `fuzzing-data` or `gh-pages`)
- ✅ Use GitHub Actions artifacts (already configured)
- ✅ Use external storage (S3, GCS) for large corpora

**Note:** The `.gitignore` is configured to exclude local corpus artifacts:

- `fuzz/corpus/` - Corpus files
- `fuzz/crashes/` - Crash-triggering inputs
- `fuzz/artifacts/` - Build artifacts
- `crash-*`, `leak-*`, `timeout-*`, `oom-*` - Fuzzer output files

### 4. Monitor for Crashes

**Never commit a crash-triggering input without fixing the bug first.**

**When a crash is found:**

1. **Reproduce the crash locally:**

   ```bash
   # ClusterFuzzLite saves crashes in artifacts
   python fuzz/fuzz_tokenize.py crash-file
   ```

2. **Debug and fix the underlying bug:**
   - Identify the root cause in the target function
   - Write a unit test that reproduces the issue
   - Fix the bug in the codebase

3. **Verify the fix:**

   ```bash
   # Re-run the fuzzer with the crash input
   python fuzz/fuzz_tokenize.py crash-file
   # Should not crash after fix
   ```

4. **Add as regression test:**

   ```python
   # In tests/test_tokenize.py
   def test_crash_regression_issue_1234():
       """Regression test for crash found by fuzzer."""
       # Use the crash-triggering input as a test case
       result = word_tokenize("...")
       assert isinstance(result, list)
   ```

5. **Only then add to corpus:**

   ```bash
   # After bug is fixed, add input to corpus for future testing
   cp crash-file fuzz/corpus/tokenize/
   ```

### Security Considerations

**Corpus storage in public gh-pages branch is safe for open-source projects:**

- ✅ Corpus contains only test inputs (strings, bytes)
- ✅ Does not contain code execution artifacts
- ✅ Follows standard OSS fuzzing practices (OSS-Fuzz, ClusterFuzzLite)

**Crash artifacts have limited exposure:**

- Uploaded as GitHub Actions artifacts (not to gh-pages)
- Have configurable retention period (default: 90 days)
- Only accessible to repository collaborators

**For private repositories with sensitive concerns:**

- Consider using a private storage-repo-branch
- Or disable corpus persistence by removing `storage-repo`
  parameters from workflow
- Fuzzing will still work, just won't persist corpus between runs

### Corpus Management Commands

```bash
# View corpus statistics
python fuzz/fuzz_tokenize.py corpus/ -runs=0

# Minimize corpus (keep unique inputs only)
python fuzz/fuzz_tokenize.py -merge=1 minimized/ corpus/

# Find minimum reproducer for a crash
python fuzz/fuzz_tokenize.py -minimize_crash=1 crash-file

# Run fuzzer with existing corpus
python fuzz/fuzz_tokenize.py corpus/ -max_total_time=60

# Check corpus coverage
python fuzz/fuzz_tokenize.py corpus/ -runs=0 -print_coverage=1
```
