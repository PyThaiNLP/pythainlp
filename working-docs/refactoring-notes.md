---
SPDX-FileCopyrightText: 2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# Refactoring notes

How to lower the complexity of a file without changing its behavior.
Phase 2 used this procedure.
Known bugs and remaining work are in [ROADMAP.md](ROADMAP.md).

## Limits

- McCabe: `max-complexity = 10` in `pyproject.toml`.
- Cognitive: `max-cognitive-complexity = 15` in `.flake8`.
- A function above a limit carries `# noqa: C901` or `# noqa: CCR001`
  with the `# phase2-todo` tag. Remove the tag when you fix the function.

## Procedure for each file

1. Measure the baseline:
   - `ruff check --isolated --disable-noqa --select C901
     --config 'lint.mccabe.max-complexity=10' <file>`
   - `flake8 --isolated --disable-noqa --select CCR001
     --max-cognitive-complexity=15 <file>`
2. Write characterization tests first. Record the outputs from the old
   code, read with `git show HEAD:<file>`.
   Pick inputs from seeded random generation by greedy arc coverage,
   plus boundary cases. Store them as golden tables in the test file.
3. Pin each bug found with a test marked `# BUG-LEDGER: <id>`.
   Add the entry to ROADMAP.md. Do not fix the bug in the refactor.
4. Refactor one function at a time.
   Use ordered lookup tables, small helpers, and early returns.
   Extract long tables from the old source with `ast`, not by hand.
   Keep the public signature and the exceptions.
5. Run a differential check against the old code.
   Use at least 30,000 seeded inputs. Compare results, exception types,
   and messages. Keep this script out of the repository.
6. Reach 100% line and branch coverage of the file:
   `python -m coverage run --branch --include=<file> -m unittest tests.core.test_x`
   then `python -m coverage report -m`.
7. Remove the `phase2-todo` noqa line.
8. Run the gates: `tox -e ruff,flake8,mypy`, doctests, and
   `python -c "import pythainlp"`.
9. Review the diff once. Never commit or push without a request.

## Traps

- Rule chains are order-sensitive. First match wins. Keep the table order
  the same as the old `if` order.
- Optional imports are lazy. Do not move them to module level.
  In `pythainlp/tokenize/__init__.py` the import order avoids a circular
  import (`# noqa: I001`). Check `import pythainlp` after each change.
- Tests of private names: load the module under a private name.
  A plain import can pollute `sys.modules` or a parent package attribute.
- Do not pin stdlib error messages. They vary by Python version.
  Assert the exception type.
- Restore the state of the stdlib `random` module in tests that seed it.
- Write Windows-safe tests: close temporary files, avoid open handles
  on directories, and avoid symlinks without a skip.
- `typing.get_type_hints()` needs runtime imports.
  Keep such imports at runtime with `# noqa: TC003` and a reason.
- `str.translate` with a dict is slow on non-ASCII text.
  A compiled regex is faster.
- Build tables at import time, not per call. Measure the import cost too.
- Benchmark old against new code: export the old tree with
  `git archive HEAD`, then run both on the same inputs.

## Shared helpers

- `pythainlp/util/_calendar.py`: Buddhist Era offset.
- `pythainlp/tag/_utils.py`: `_iob_to_markup`.
- `pythainlp/tokenize/_registry.py`: engine adapters and aliases.

## What remains

See "Remaining refactoring work" in [ROADMAP.md](ROADMAP.md).
