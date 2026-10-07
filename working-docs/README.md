---
SPDX-FileCopyrightText: 2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# Working documents

This directory holds working notes for maintainers and AI agents.
It is not user documentation.
The package does not ship it: the sdist `include` list in `pyproject.toml`
is explicit and omits this directory.

## Files

- [ROADMAP.md](ROADMAP.md): known bugs, security notes, and
  remaining refactoring work.
- [refactoring-notes.md](refactoring-notes.md): how to refactor a file
  safely, and the traps found so far.

## Rules

- Record each bug found during refactoring in `ROADMAP.md`.
  Pin it with a test marked `# BUG-LEDGER: <id>`.
- Keep notes short and current.
- Delete a note when its work is done.
