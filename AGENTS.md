# Instructions for AI agents

## PyThaiNLP specific

- Follow the test categories, dependency sets, and test naming conventions in
  <https://github.com/PyThaiNLP/pythainlp/blob/dev/tests/README.md>.
- Follow NLTK conventions for submodule names (a verb or a generic noun),
  function names, and configuration when possible, and tell the user about
  it during code review. See <https://www.nltk.org/py-modindex.html>.
- Naming: PEP 8, concise, US spelling. Align new modules, classes, public
  APIs, and environment variables with NLTK first, if they suit the
  component. If NLTK has no precedent, follow spaCy, CoreNLP/Stanza,
  LangPipe, then Hugging Face.
- Number: use singular names for a class that represents one entity.
  Use plural names only for collections, utility modules, or aggregates.
- Error and warning messages: clear, concise, consistent in style, and
  parseable.
- Do not use `os.path.join()`. Use `pythainlp.tools.safe_path_join()` to
  prevent path traversal (CWE-22).
- API documentation is in `docs/api/`. Each module needs an `.rst` file so
  its API documentation is public.
- Log major changes in
  <https://github.com/PyThaiNLP/pythainlp/blob/dev/CHANGELOG.md>
  (see "Change log" below).
- Known issues and planned work are in
  <https://github.com/PyThaiNLP/pythainlp/blob/dev/working-docs/ROADMAP.md>.
  Other working notes are in `working-docs/`.
  - Record each bug found while working on something else there, with a
    test that pins the current behavior.
  - Do not fix such a bug in an unrelated or behavior-preserving change.
    Fix it in its own pull request.

### Docstrings

Use reStructuredText (PEP 287) for Sphinx. The docstring and its doctest
must match the latest code.

- Layout (Codacy enforces pydocstyle D213; its settings cannot change):
  - Use `"""`. A one-line docstring stays on one line.
  - A multi-line docstring starts its summary on the second line.
  - The summary is one sentence in the imperative mood ("Convert ...",
    "Return ..."), ending with a period.
  - Then a blank line, an optional description, a blank line, the fields,
    a blank line, and `:Example:`.
  - Keep every line within 79 characters, indent included. Exceptions: a
    URL, and a doctest output line that cannot wrap.
  - Do not end a docstring line with a backslash; it joins lines.
- Fields, in this order: `:param <type> <name>:`, `:return:`, `:rtype:`,
  `:raises <Exception>:`.
  - Write the type as in the annotation, with built-in generics
    (`list[str]`) and fully qualified names for non-stdlib types
    (`numpy.ndarray`, `pandas.DataFrame`), so the module is clear.
  - A field description is a phrase that starts in lowercase, with no final
    period. A description of several sentences uses capitalized sentences
    with periods.
  - Indent the continuation of a field by 4 spaces.
  - List options as `* *name* - description` under the field, indented by
    4 spaces. Mark the default with `(default)`.
- Wording: US spelling, active voice, parallel phrasing between similar
  functions. Use the same terms everywhere: "text" (a `str` to process),
  "word" (a token), "list of words", "engine" (an algorithm or model
  option), "corpus", "tokenize", and "Thai" (capitalized).

## Tests and quality

Leave every file you touch better than you found it.

- Coverage:
  - Expected overall coverage is at least 80%. A PR must not drop it by more
    than 0.1%.
  - New and changed code needs at least 95% coverage. CI (`diff-cover`)
    gates it, except in the noauto modules listed in
    `tests/diff-cover-noauto.txt`. CI cannot run those modules (their
    dependencies, such as torch, are not installed), so it only reports
    their coverage. Run the noauto test suites locally and meet the same
    95%.
  - Agents should aim for near 100% line and branch coverage of the code
    they add or change, and cover every function they touch.
- Add tests for new behavior, covering all branches and edge cases.
- Write compact tests: use parameterized tests (`subTest` or table-driven
  cases) instead of many near-identical methods.
- Add characterization tests before refactoring, to record the current
  behavior.
- Add a regression test for every bug fix.
- Add adversarial tests: empty input, `None`, wrong types, Unicode edge
  cases, very long input, and boundary values.
- Use `# type: ignore[arg-type]` in tests only when the test checks type
  handling or `TypeError`.
- Keep complexity within the limits: McCabe 10 and cognitive 15 (flake8 with
  flake8-cognitive-complexity, see `.flake8`). Refactor a touched function
  that exceeds them, or at least do not make it more complex. Functions not
  yet refactored carry `# noqa: CCR001` (or `# noqa: C901` for McCabe) and
  a `# phase2-todo` tag.
- Keep code maintainable: small functions, lookup tables instead of long
  `if` chains, shared helpers instead of copied blocks.
- Prefer the smallest change. Keep refactoring behavior-preserving.
- Follow the project's coding style. Run Ruff and `ruff format` (CI enforces
  both) and fix the errors before committing. Write new code to pass all
  Ruff checks, and improve existing code gradually when you change it.
- After changes, review code and documentation for correctness,
  consistency, and clarity. Comments, APIs, and documentation must match
  the code, and documentation examples must run.

## Change log

Update `CHANGELOG.md` for significant changes.

- Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
  [semantic versioning](https://semver.org/).
- Mark a breaking change clearly, and give migration instructions if needed.
- Keep entries concise, without background or rationale (the PR has them).
  Aim at about 140 characters; a complex PR may exceed it.
- End each entry with its PR link, as in
  <https://github.com/bact/pitloom/blob/main/CHANGELOG.md>: `([#123])`,
  with the `[#123]: <PR URL>` definitions at the end of each release
  section.
- Merge related PRs into one entry: `([#1], [#2])`. Sort the entries in a
  section by their lowest PR number.
- Skip documentation-only, version bump, and CI-only changes.

## Language and style

- Write short, simple comments. Do not state the obvious or restate the
  code.
- Use clear, concise, unambiguous sentences in the active voice, with
  correct grammar, punctuation, and American English spelling.
- Avoid jargon, slang, idioms, unnecessary complexity, and words with more
  than one interpretation.
- Use consistent terminology. Define acronyms on first use. Use technical
  terms accurately.
- Use consistent formats for dates, times, numbers, and units. Use SI
  abbreviations for units.
- Break long paragraphs into smaller ones, bullets, or numbered lists.
  Separate distinct concepts, processes, criteria, and categories.
- Use parallel structure in lists, and a uniform style for related
  information, so readers can compare.
- Use "sentence case" for headings and titles.
- Format code snippets by the conventions of their language.
- Use Chicago style for references, unless told otherwise.
- Use the verbal forms of requirement levels consistently: IETF (RFC 2119,
  RFC 8174) by default for internet, web, and semantic web projects; ISO/IEC
  (ISO/IEC Directives, Part 2) for SPDX. Detect the level from the domain of
  the document.
- Names: follow the conventions of the language and framework. Use only
  ASCII letters, digits, hyphen (-), and underscore (_).
- URLs/IRIs: lowercase letters and hyphens (`my-api-endpoint`), following
  [Cool URIs](https://www.w3.org/TR/cooluris/).
- Consult Schema.org vocabularies and "Style Guidelines for Naming and
  Labeling Ontologies in the Multilingual Web"
  (<https://www.researchgate.net/publication/277224472>) when choosing
  names.
- Use linters and formatters where applicable.
- Do not leave trailing whitespace, unless it is necessary.

## Project metadata and file headers

- Keep `pyproject.toml`, `codemeta.json`, `CITATION.cff`, and other
  metadata files consistent and up to date: project name, version,
  author/contributor names, license, description, repository URL, and
  keywords (in the same order if possible).
- Put SPDX file tags in file headers when possible, sorted:
  `SPDX-FileContributor`, `SPDX-FileCopyrightText`, `SPDX-FileType`
  (default `SOURCE` for code, `DOCUMENTATION` for documentation), and
  `SPDX-License-Identifier` (default `Apache-2.0` for code, `CC0-1.0` for
  documentation).
  See <https://spdx.github.io/spdx-spec/v2.3/file-information/>.

## Cross-platform support

PyThaiNLP targets Windows, Linux, and macOS. CI tests all three.

- Paths: use `pathlib` or `pythainlp.tools.safe_path_join()`. Do not
  hardcode `/` or `\`, `/tmp`, a drive letter, or the home directory layout.
  Windows paths have a length limit, reserved names (`NUL`), 8.3 short names
  (`RUNNER~1`), and are case-insensitive. Compare paths after
  `os.path.realpath()`.
- Files: pass `encoding=` to `open()`. Close a file before replacing or
  deleting it; Windows raises `PermissionError`. Symbolic links and
  permission bits are limited on Windows.
- Encoding: the default differs by platform (Windows uses a legacy code
  page, such as cp874 or cp1252, until Python 3.15).
  - Use UTF-8 for Thai text, source files, and data files. Use `utf-8-sig`
    to read a file that may start with a BOM.
  - Do not assume `print()` can write Thai: a Windows console or a
    redirected stream may raise `UnicodeEncodeError`. Do not depend on
    `sys.stdout.encoding` or `locale`.
  - Do not compare Thai strings as bytes. Count and slice code points, not
    bytes or user-perceived characters (a combining mark is its own code
    point).
  - macOS can normalize non-ASCII file names (NFD). Do not rely on an exact
    round trip; keep file names in ASCII.
- Signals: catch `KeyboardInterrupt`, not a signal number. Windows lacks
  `SIGKILL`, `SIGHUP`, and `SIGALRM`.
- Processes: `multiprocessing` uses `spawn` on Windows and macOS. Guard the
  entry point and keep arguments picklable.
- Environment variables are case-insensitive on Windows only. Use
  `pathlib.Path.home()`, not `HOME`.
- Prefer a feature check (`hasattr`, `try`/`except`) over a platform check.
  Otherwise use `sys.platform` or `os.name`.
- Keep optional native dependencies (ICU, PyTorch) out of the core install.
- Tests:
  - Do not record expected values on one platform only. For example,
    Windows rejects `time.strftime()` directives such as `%-d`.
  - Use `tempfile`; do not write to the working directory.
  - Use `unittest.skipIf` with a reason for a platform-specific test.

## Shell scripts and command line

- Mind the differences between GNU, BSD, and macOS tools. For example,
  `sed -i` needs an argument on BSD but not on GNU; `date`,
  `readlink -f`, `xargs`, and `grep -P` also differ. Prefer POSIX options,
  or write the step in Python.
- Mind the differences between shells (bash, zsh, PowerShell, `cmd`):
  quoting, escaping, unmatched globs (zsh fails), and variable syntax
  (`$VAR`, `%VAR%`, `$env:VAR`). In GitHub Actions, set `shell:` when it
  matters.
- Be defensive on variable expansion. Quote paths. Mind the semantics of
  different quotation marks.

## Dependencies and imports

- Check library, module, and package names carefully: beware of
  slopsquatting and typosquatting.
- Use the latest library version that the OS, compiler, or framework
  supports. Check that a suggested version exists and is compatible.
  Prefer semantic versions.
- Warn about abandoned dependencies and suggest drop-in replacements.
- Sort dependencies in build metadata (such as `pyproject.toml`).
- Group and sort imports by language convention (in Python: standard
  library, then third-party, then alphabetical). Keep an order that a
  dependency requires, and do not introduce circular imports; read the
  comments near imports. Remove unused imports.

## Security

- Follow the principle of least privilege.
- Avoid deprecated, obsolete, or insecure libraries, frameworks, and APIs.
- Protect sensitive data (passwords, API keys, personal data). Do not
  hardcode secrets.
- Validate and sanitize all user input (SQL injection, XSS, buffer
  overflows).
- Update dependencies to their latest secure versions regularly.
- Use strong, well-established algorithms and key sizes for cryptography.
- Follow standards such as OAuth2 and OpenID Connect for authentication and
  authorization.
- Avoid `eval()` and similar functions, unless necessary and safe.
- Avoid deserializing untrusted data (CWE-502). In Python, avoid `pickle`.
- Be careful of path traversal (CWE-22).

## API

- Follow the latest OpenAPI specification (<https://spec.openapis.org/oas/>)
  and web best practices from OpenAPI, IETF, and W3C.
- Use proper HTTP return codes.

## Git

- Write commit messages by
  [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/).
- At the end of a set of file changes, or at any other good commit
  opportunity, offer a commit message. Do not commit unless asked. Give two
  versions, each in its own fenced code block, so each has a copy button:
  - A one-line version: plain text, no Markdown, under 60 characters.
  - A longer version: a subject line, a blank line, then a body that may
    use Markdown, such as bullets and `code` spans.
- When asked for a pull request (PR) title, summary, description, or change
  log entry, give each in its own fenced Markdown code block, so it can be
  copied. Default lengths when none is given:
  - PR title: under 60 characters (usable as a commit message)
  - PR summary: under 280 characters, as bullets
  - PR description: under 1000 characters
  - Change log entry: under 140 characters per entry

## Python

- Keep code readable and idiomatic.
- Keep configuration in `pyproject.toml` when possible, in modern TOML.
- Code defensively: check for `None` and empty values and handle exceptions
  for external input (arguments, file I/O, network I/O).
- Do not use `assert` in production code: Python removes it under `-O`.
  Raise an exception (`ValueError`, `TypeError`, ...) instead. Ruff `S101`
  enforces this; `assert` is fine in tests.
- Do not use mutable default arguments or wildcard imports.
- Make the package zip-safe if possible.
- `requires-python` in `pyproject.toml` is the minimum supported version.
  Do not use syntax or features it does not support, unless a `__future__`
  import provides them. Do not use `A | B` union syntax below Python 3.10.
- Sort the members of a collection literal (list, set, tuple, dict keys,
  `__all__`) when possible, even for a set. Keep the order when it matters
  at run time, including an order that gives an early exit or early hit for
  common cases, and add a short comment.
- Prefer built-in data structures (list, dict, set, tuple). Use `collections`
  or `collections.abc` types when needed, and pick the structure that suits
  the performance and memory needs.
- Package metadata follows the
  [Core metadata specifications](https://packaging.python.org/en/latest/specifications/core-metadata/).

### Type annotations

- Annotate every function, method, class, and variable as completely as
  possible, following standard type hint patterns, and keep near-100%
  coverage. Annotations must work for runtime inspection and documentation
  tools (`typing.get_type_hints()`, `inspect`).
- Use mypy as an assistant (it is in the "dev" extra; reset its cache if it
  reports unexpected errors). Use pyright, pyrefly, and pytype for second
  opinions.
- Use the type analyzer
  <https://github.com/PyThaiNLP/pythainlp/blob/dev/build_tools/analysis/type-analyzer.py>
  to check annotation completeness. See
  <https://github.com/PyThaiNLP/pythainlp/blob/dev/build_tools/analysis/README.md>.
  It can report false positives; check the
  [Python type specification](https://typing.python.org/en/latest/spec/).
- Put typing imports in an `if TYPE_CHECKING:` block when possible (Ruff
  `TC` rules enforce this). If an import must stay at runtime, for example
  to keep `typing.get_type_hints()` working, add `# noqa: TC00x` with the
  reason.
- Minimize `Any`. Look for type stubs or the library's source (GitHub,
  GitLab, Codeberg; find the repository from PyPI metadata).
- Recheck whether each cast, `# noqa:`, and `# type: ignore` is needed.
- Keep docstrings consistent with the updated type hints.

Type completeness follows
[the typing guide](https://typing.python.org/en/latest/guides/libraries.html#type-completeness):

- Classes: annotate all visible (not overridden) class variables, instance
  variables, and methods with known types. Give type arguments for each
  generic parameter of a generic base class.
- Functions and methods: annotate all parameters and the return value with
  known types. A decorated function must still have a known type.
- Type aliases: all referenced types are known.
- Variables: all annotated with known types.

You may omit an annotation when the type is obvious:

- A constant with a simple literal value (`MAX_TIMEOUT = 50`,
  `room_temperature: Final = 20`). A constant is assigned once and is
  annotated `Final` or named in all caps. A constant with a non-literal
  value needs an annotation, preferably with `Final`
  (`WOODWINDS: Final[list[str]] = ["Oboe", "Bassoon"]`).
- `Enum` values.
- A type alias: one module-level assignment of an instantiable type
  (`Bar = MyGenericClass[int] | None`).
- `self` and `cls`, and the `None` return of `__init__`.
- Module-level `__all__`, `__author__`, `__copyright__`, `__email__`,
  `__license__`, `__title__`, `__uri__`, `__version__`, and class-level
  `__class__`, `__dict__`, `__doc__`, `__module__`, `__slots__`.

## JSON, Markdown, diagrams, HTML, and CSS

- JSON: valid and well-formatted. Enclose decimal values (such as
  `xs:decimal`) in quotes, to keep the type and precision.
- Markdown: put metadata as YAML between triple-dashed lines (as Hugo and
  Jekyll front matter). Be strict and use standard Markdown; what works on
  GitHub may not work on MkDocs. Fix problems that Markdownlint reports.
- ASCII/text diagrams: count characters and adjust spaces so the lines
  align.
- HTML: valid and well-formatted, with no trailing whitespace. Follow W3C
  accessibility recommendations when possible.
- HTML and CSS: use sensible, concise element IDs and names; grouping names
  helps readability. CSS has no unused styles.
