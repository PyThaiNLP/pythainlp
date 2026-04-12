---
SPDX-FileCopyrightText: 2025-2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# Contributing to PyThaiNLP

Hi! Thanks for your interest in contributing to
[PyThaiNLP](https://github.com/PyThaiNLP/pythainlp).

Please refer to our
[Contributor Covenant Code of Conduct](https://github.com/PyThaiNLP/pythainlp/blob/main/CODE_OF_CONDUCT.md).

## Issue report and discussion

- Discussion: <https://github.com/PyThaiNLP/pythainlp/discussions>
- GitHub issues (for problems and suggestions):
  <https://github.com/PyThaiNLP/pythainlp/issues>
- Facebook group (for general Thai NLP discussion, not specific to PyThaiNLP):
  <https://www.facebook.com/groups/thainlp>

## Code

## Code guidelines

- Follow [PEP8][pep8], use [black][black] with `--line-length` = 79;
- Name identifiers (variables, classes, functions, module names)
  with meaningful and pronounceable names (`x` is always wrong);
  - Please follow this [naming convention][naming].
    For example, global constant variables must be in `ALL_CAPS`;
    ![Naming Convention](https://i.stack.imgur.com/uBr10.png)
- Write tests for your new features.
  The test suite is in `tests/` directory.
  (see "Testing" section below);
- Run all tests before pushing (just execute `tox`) so you will
  know if your changes broke something;
- Commented-out code is [dead code][dead-codes];
- All `#TODO` comments should be turned into [issues][issues] in GitHub;
- When appropriate, use [f-string][pep0498]
  (use `f"{a} = {b}"`,
  instead of `"{} = {}".format(a, b)` and `"%s = %s' % (a, b)"`);
- All text files, including source codes, must end with one empty line.
  This is [to please Git][empty-line] and
  [to keep up with POSIX standard][posix].

[pep8]: https://peps.python.org/pep-0008/
[black]: https://github.com/ambv/black
[naming]: https://namingconvention.org/python/
[pep0498]: https://www.python.org/dev/peps/pep-0498/
[dead-codes]: https://blog.codinghorror.com/coding-without-comments/
[issues]: https://github.com/pythainlp/pythainlp/issues
[empty-line]: https://stackoverflow.com/questions/5813311/no-newline-at-end-of-file#5813359
[posix]: https://stackoverflow.com/questions/729692/why-should-text-files-end-with-a-newline

### Error messages, warnings, and exception handling

Clear, consistent, and parseable error and warning messages help users
debug problems and allow tooling to parse and filter output.
Follow these conventions in all PyThaiNLP code.

#### Exception types

Use the most specific built-in exception type for each situation:

| Situation | Exception type |
| --- | --- |
| Missing optional dependency at import time | `ImportError` or `ModuleNotFoundError` |
| Invalid argument value | `ValueError` |
| Wrong argument type | `TypeError` |
| Required file not found | `FileNotFoundError` |
| I/O or OS-level failure | `OSError` |
| Runtime failure with no more-specific type | `RuntimeError` |
| Feature not yet implemented | `NotImplementedError` |

#### Exception message format

Write messages as complete sentences.

- End each sentence with a period.
- Identify the offending value, name, or path explicitly.
- For a missing optional dependency, include the `pip install` command:

  ```text
  <Package> is not installed. Install it with: pip install <package>
  ```

  If the package is a PyThaiNLP optional-dependency group, name the extra:

  ```text
  <Package> is required for this feature.
  Install it with: pip install pythainlp[<extra>]
  ```

- For an invalid argument value, name the parameter and show the received value:

  ```text
  <param> must be <description>; got {value!r}
  ```

#### Exception forwarding (chaining)

Always chain exceptions with `from` when raising a new exception inside an
`except` block, so the full traceback and original cause are preserved:

```python
# Correct: chain to the original exception.
try:
    import some_package
except ImportError as e:
    raise ImportError(
        "some_package is not installed. Install it with: pip install some_package"
    ) from e

# Correct: suppress chain with `from None` only when the original
# exception is irrelevant noise that would confuse the user.
raise ValueError("Invalid configuration value.") from None
```

Never use `raise e` to re-raise a caught exception. Use bare `raise` instead,
which preserves the original traceback:

```python
# Correct: bare re-raise preserves traceback.
except Exception:
    log_or_print_something()
    raise

# Incorrect: `raise e` creates a new traceback starting at this line.
except Exception as e:
    log_or_print_something()
    raise e  # do not do this
```

When re-raising as a *different* exception type, always supply `from`:

```python
# Correct.
except OSError as e:
    raise RuntimeError(f"Failed to read model file: {e}") from e

# Incorrect: original cause is silently discarded.
except OSError as e:
    raise RuntimeError(f"Failed to read model file: {e}")
```

#### Warnings

Use `warnings.warn()` for non-fatal conditions that the caller should know
about. Always pass both `category` and `stacklevel` explicitly:

```python
import warnings

warnings.warn("Message.", UserWarning, stacklevel=2)
```

Recommended categories:

| Situation | Category |
| --- | --- |
| Deprecated API that will be removed in a future version | `DeprecationWarning` |
| Skipped or degraded behavior the caller should review | `UserWarning` |

Use `stacklevel=2` so the warning points at the **caller's** line, not the
internal line that called `warnings.warn()`. Increase `stacklevel` by one for
each additional layer of indirection between the public API and the
`warnings.warn()` call.

Warning messages should be clear, concise, and parseable:

- Write messages as complete sentences ending with a period.
- For deprecations, name the deprecated symbol and its replacement:

  ```text
  <old_symbol> is deprecated; use <new_symbol> instead.
  ```

- For skipped data or fallback behavior, describe what was skipped and why:

  ```text
  Skipping <item> entry with <reason>: {value!r}
  ```

Do **not** rely on the default `UserWarning` by omitting `category`.
Always supply `category` explicitly for clarity and greppability.

### Version control system

- We use [Git](https://git-scm.com/) as our
  [version control system](https://en.wikipedia.org/wiki/Revision_control),
  so it may be a good idea to familiarize yourself with it.
- You can start with the [Pro Git book](https://git-scm.com/book/) (free!).

### Commit message

- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Commit Verbs 101: why I like to use this and why you should also like it.](https://chris.beams.io/posts/git-commit/)

### Pull request

- We use the famous [gitflow][] to manage our branches.
- When you create pull requests on GitHub, GitHub Actions will run tests
  and several checks automatically. Click the "Details" link
  at the end of each check to see what needs to be fixed.

[gitflow]: https://nvie.com/posts/a-successful-git-branching-model/

## Documentation

- We use [Sphinx](https://www.sphinx-doc.org/en/master/) to generate
  API document automatically from "docstring" comments in source codes.
  This means the comment section in the source codes is important for the
  quality of documentation.
- A docstring should start with one summary line, end with one line with
  a full stop (period), then be followed by a blank line before starting
  a new paragraph.
- A commit to release branches (e.g. `2.2`, `2.1`) with a title
  **"(build and deploy docs)"** (without quotes) will trigger the system
  to rebuild the documentation files and upload them to the website
  <https://pythainlp.org/docs>.

## Testing

We use standard Python `unittest`.
The test suite is in `tests/` directory.

To run unit tests locally together with code coverage test:

(from main `pythainlp/` directory)

```sh
coverage run -m unittest tests.core
```

See code coverage test:

```sh
coverage report
```

Generate code coverage test in HTML
(files will be available in `htmlcov/` directory):

```sh
coverage html
```

Make sure the tests pass on GitHub Actions.

See more in [tests/README.md](./tests/README.md)

## Installing and building

### Installing for development

Install PyThaiNLP in editable mode with core dependencies:

```sh
pip install -e .
```

Install with optional dependency groups:

```sh
# Install with compact set of dependencies (recommended for development)
pip install -e ".[compact]"

# Install with extra set of dependencies (can be huge)
pip install -e ".[compact,extra]"
```

See all available optional dependency groups in `pyproject.toml`
under `[project.optional-dependencies]`.

### Building distribution packages

To build source distribution and wheel:

```sh
python -m build
```

This will create distribution packages in the `dist/` directory.

## Releasing

- We use [Semantic Versioning][semver]: MAJOR.MINOR.PATCH,
  with development build suffix: MAJOR.MINOR.PATCH-devBUILD
- We use [`bump-my-version`][bump-my-version]
  to manage versioning. The configuration is in `pyproject.toml`
  under `[tool.bumpversion]`.
  - `bump-my-version bump [major|minor|patch|release|build]`
  - Example:

  ```sh
  #current_version = 2.3.3-dev0

  bump-my-version bump build
  #current_version = 2.3.3-dev1

  bump-my-version bump build
  #current_version = 2.3.3-dev2

  bump-my-version bump release
  #current_version = 2.3.3-beta0

  bump-my-version bump release
  #current_version = 2.3.3

  bump-my-version bump patch
  #current_version = 2.3.4-dev0

  bump-my-version bump minor
  #current_version = 2.4.0-dev0

  bump-my-version bump build
  #current_version = 2.4.0-dev1

  bump-my-version bump major
  #current_version = 3.0.0-dev0

  bump-my-version bump release
  #current_version = 3.0.0-beta0

  bump-my-version bump release
  #current_version = 3.0.0
  ```

- Read the full [how to cut a new release](./release.md) documentation.

[semver]: https://semver.org/
[bump-my-version]: https://github.com/callowayproject/bump-my-version

## Credits

[![Contributors](https://contributors-img.firebaseapp.com/image?repo=PyThaiNLP/pythainlp)](https://github.com/PyThaiNLP/pythainlp/graphs/contributors)

Thanks to all
[contributors](https://github.com/PyThaiNLP/pythainlp/graphs/contributors).
(Image made with [contributors-img](https://contributors-img.firebaseapp.com))

### Development leads

- Wannaphong Phatthiyaphaibun <wannaphong@pythainlp.org> - foundation,
  distribution and maintenance
- Korakot Chaovavanich - initial tokenization and soundex codes
- Charin Polpanumas - classification and benchmarking
- Arthit Suriyawongkul - localization functions, documentation, security,
  tests, refactoring, code modernization, and CI/build infrastructure
- Lalita Lowphansirikul - documentation
- Pattarawat Chormai - benchmarking
- Peerat Limkonchotiwat
- Thanathip Suntorntip - nlpO3 maintenance, Rust developer
- Can Udomcharoenchaikit - documentation and codes

### Maintainers

- Arthit Suriyawongkul
- Wannaphong Phatthiyaphaibun

### Past

- Peeradej Tanruangporn - documentation

## References

- **[Maximum matching]** --
  Manabu Sassano. Deterministic Word Segmentation Using Maximum
  Matching with Fully Lexicalized Rules.
  Retrieved from
  <https://doi.org/10.3115/v1/E14-4016>
- **[MetaSound]** --
  Snae & Brückner. (2009).
  Novel Phonetic Name Matching Algorithm with a Statistical
  Ontology for Analysing Names Given in Accordance with
  Thai Astrology.
  Retrieved from
  <https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf>
- **[Thai Character Cluster]** --
  T. Teeramunkong, V. Sornlertlamvanich, T. Tanhermhong and W. Chinnan,
  “Character cluster based Thai information retrieval,”
  in IRAL '00 Proceedings of the fifth international workshop
  on Information retrieval with Asian languages, 2000.
- **[Enhanced Thai Character Cluster]** --
  Jeeragone Inrut, Patiroop Yuanghirun, Sarayut Paludkong,
  Supot Nitsuwat, and Para Limmaneepraserth.
  “Thai word segmentation using combination of forward and backward
  longest matching techniques.”
  In International Symposium on Communications and Information
  Technology (ISCIT), pp. 37-40. 2001.
- **[Thai Stopword List]** --
  เพ็ญศิริ ลี้ตระกูล.
  การเลือกประโยคสำคัญในการสรุปความภาษาไทย โดยใช้แบบจำลองแบบลำดับชั้น
  (Selection of Important Sentences in Thai Text Summarization
  Using a Hierarchical Model).
  Retrieved from
  <https://digital.library.tu.ac.th/tu_dc/frontend/Info/item/dc:124897>
- **[Thai Discourse Treebank]** --
  Ponrawee Prasertsom, Apiwat Jaroonpol, Attapol T. Rutherford;
  The Thai Discourse Treebank: Annotating and Classifying Thai
  Discourse Connectives.
  Transactions of the Association for Computational Linguistics 2024;
  12 613–629.
  doi: <https://doi.org/10.1162/tacl_a_00650>
