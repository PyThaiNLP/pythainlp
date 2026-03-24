# Instructions for AI agents

## PyThaiNLP specific

- [ ] Follow test suite categorization and test matrix in
      <https://github.com/PyThaiNLP/pythainlp/blob/dev/tests/README.md>.
      The document list test categories, their dependency sets,
      and test naming conventions.
- [ ] Use reStructuredText for docstring (PEP 287), targeting Sphinx.
- [ ] When possible, follow NLTK established convention of submodule
      name (tend to be a verb or a generic noun), function name, and
      configuration. Communicate this to the users during code review.
      See <https://www.nltk.org/py-modindex.html>.
- [ ] The type information analyzer at
      <https://github.com/PyThaiNLP/pythainlp/blob/dev/build_tools/analysis/type-analyzer.py>
      can generate information about annotation completeness of
      variables, functions, methods, type aliases, decorators, and
      classes in the PyThaiNLP repo.
      Use it to assist the maintenance of 100% type completeness in
      the repo. Read its usage and information it generates at
      <https://github.com/PyThaiNLP/pythainlp/blob/dev/build_tools/analysis/README.md>.
      Mind that the analyzer can create false positives,
      please refer to Python type specification when in doubt.
- [ ] Complete type annotations for function, method, class, variable, etc.
      Maintain near-100% type annotation coverage.
- [ ] Add tests for new functionality or behavior.
      New PR must not drop the test coverage more than 0.1%.
- [ ] Keep the test coverage high. Aim at least 70% test coverage.
- [ ] Add test cases to cover all code branches and capture edge cases.
- [ ] `# type: ignore[arg-type]` comment can be used in the test code,
      only if that specific code want to explicitly test type handling
      or TypeError raising.
- [ ] Docstring and doctest must reflect the latest code.
- [ ] All error messages and warning messages should be clear, concise,
      and consistent in style. They should be parseable.
- [ ] API documentation is in docs/api/.
      There must be an .rst file for each module, so that the generated
      module API documentation is visible publicly.
- [ ] Major changes should be logged in the change log at
      <https://github.com/PyThaiNLP/pythainlp/blob/dev/CHANGELOG.md>.
      Provide issue number or PR number if available.
- [ ] Do not use os.path.join();
      always use pythainlp.tools.safe_path_join() instead,
      to prevent path traversal vulnerabilities (CWE-22).
- [ ] Naming conventions: Follows PEP 8. Concise. Use US spelling.
      Align new modules, classes, public APIs, and environment
      variables with NLTK conventions as the primary standard,
      provided they suit the component's behavior.
      If NLTK offers no clear precedent, defer to established NLP
      frameworks in the following order of preference:
      spaCy, CoreNLP/Stanza, LangPipe, and Hugging Face.
- [ ] Noun number consistency: Maintain strict intentionality
      regarding singular vs. plural forms. Use singular names for
      classes representing a single entity and reserve plural
      names only for collections, utility modules, or clear aggregates.

## Project contribution guidelines

- [ ] Follow the project's established coding style and conventions.
- [ ] Run Ruff and fix errors before committing code.
  - [ ] New code should be written to pass all Ruff checks.
  - [ ] McCabe complexity should be kept low;
        refactor the new code that exceeds 10.
  - [ ] Cognitive complexity should be kept low;
        refactor the new code that exceeds 15.
  - [ ] Existing code should be gradually improved to pass Ruff checks
        when making changes.
- [ ] Write clear and concise commit messages that accurately describe
      the changes made.
- [ ] For significant changes, update the CHANGELOG.md file
      to document the changes.
  - [ ] Follow "Keep a Changelog" style guide
        <https://keepachangelog.com/en/1.1.0/>
  - [ ] Use semantic versioning for version numbers
        <https://semver.org/>
  - [ ] If it is a breaking change, indicate it clearly in the changelog.
    - [ ] Provide migration instructions if necessary.
- [ ] Do not leave trailing whitespaces in the code or documentation files,
      unless such a whitespace is explicitly necessary.
- [ ] Metadata in pyproject.toml, codemeta.json, CITATION.cff, and other
      project metadata files should be consistent and up-to-date.
  - [ ] Project name
  - [ ] Project version
  - [ ] Author/contributor names
  - [ ] License information
  - [ ] Project description
  - [ ] Repository URL
  - [ ] Keywords/tags (in the same order if possible)

## General language use

- [ ] Write short and simple comments. Do not state the obvious.
- [ ] Prefer clear, concise, and unambiguous sentences.
- [ ] Do not use jargon, slang, or idiomatic expressions
      that may not be universally understood.
- [ ] Use active voice whenever possible.
- [ ] Use consistent terminology throughout the code and documentation.
- [ ] Define acronyms and abbreviations on their first use.
- [ ] Use technical terms accurately and appropriately.
- [ ] Avoid unnecessary complexity and verbosity.
- [ ] Use proper grammar, punctuation, and spelling.
- [ ] Use consistent formatting for dates, times, numbers, and units of measure.
- [ ] When using abbreviations for units of measure, follow the International
      System of Units (SI) conventions.
- [ ] When using code snippets, ensure they are properly formatted and
      follow the conventions of the programming language being used.
- [ ] Avoid words and phrases that may have more than one interpretation.
- [ ] Avoid overly long paragraphs. Breaking up text into smaller paragraphs,
      using bullet points, or creating numbered lists to improve readability.
- [ ] Help readers' comprehension by separating distinct concepts, processes,
      criteria, or categories.
- [ ] Use parallel language structures in lists and documentation.
- [ ] Use a uniform writing style, particularly when presenting similar or
      related information, so the reader can compare easily.
- [ ] If not specified otherwise, use Chicago style for reference/citation.
- [ ] When writing on level of requirements, use the verbal forms consistently.
      Use either ISO/IEC verbal form (ISO/IEC Directives, Part 2 --
      Principles and rules for the structure and drafting of ISO and IEC
      documents) or IETF verbal form (RFC 2119 and RFC 8174).
      Try to detect the level of requirements from type/domain of the document.
      IETF is default for internet/web/semantic web projects in general.
      ISO is default for SPDX project.
- [ ] Use American English spelling consistently.

## Naming conventions

- [ ] Follow standard naming conventions for the programming language
      and framework you are using.
- [ ] Use only ASCII letters, digits, hyphen (-), and underscore (_)
      in names.
- [ ] For URLs/IRIs, use lowercase letters and hyphens to separate words
      (e.g., `my-api-endpoint`) and follow W3C Cool URIs for the Semantic Web:
      <https://www.w3.org/TR/cooluris/>
- [ ] Consult Schema.org vocabularies when deciding about names.
- [ ] Consult "Style Guidelines for Naming and Labeling Ontologies in the
      Multilingual Web" <https://www.researchgate.net/publication/277224472>

## Tidy code and documentation

- [ ] Ensure that the code is well-formatted and adheres to the style
      guidelines of the programming language you are using.
- [ ] Use linters and formatters where applicable.
- [ ] Use "sentence case" for headings and titles in documentation.
- [ ] Write clear and concise comments and documentation for your code.
      For something obvious, avoid comments that just restate the code.
- [ ] After making changes, review the code and documentation to ensure
      up-to-dateness, correctness, consistency, and clarity.
- [ ] Make sure that all code comments, APIs, and documentation are consistent
      with the current state of the codebase.
- [ ] Make sure that the examples in the documentation are runnable, up-to-date
      and reflect the current behavior of the code.

## File header

- [ ] When possible, put relevant SPDX File Tags at file header.
      See <https://spdx.github.io/spdx-spec/v2.3/file-information/>
  - [ ] SPDX-FileContributor
  - [ ] SPDX-FileCopyrightText
  - [ ] Default SPDX-FileType for code is "SOURCE"
  - [ ] Default SPDX-FileType for documentation is "DOCUMENTATION"
  - [ ] Default SPDX-License-Identifier for code is "Apache-2.0"
  - [ ] Default SPDX-License-Identifier for documentation is "CC0-1.0"
  - [ ] Sort SPDX metadata.

## Shell scripts and command line

- [ ] Mind the differences between GNU, BSD, macOS,
      and other implementations of common Unix tools.
- [ ] Be defensive on variable expansion.
- [ ] Use quotes or other constructs to encapsulate paths, make it compatible
      with different kinds of shells.
- [ ] Be mindful about the semantics of different types of quotation marks.

## Library imports and dependencies

- [ ] Check the correctness of library/module/package names.
      Be very careful of slopsquatting and typosquatting attacks.
- [ ] Use the most updated version of the library that is supported
      by the OS/compiler/framework currently being used.
- [ ] In source code, group and sort imports by the programming language
      convention (e.g., in Python, typically by standard library first,
      then by third-party libraries)
      and then by alphabetical order whenever possible.
      Be careful of specific order of import requirements of some dependencies,
      as moving the order may break the code or create cyclic import issues.
- [ ] Remove unused imports.
- [ ] In build metadata (like pyproject.toml in Python) or
      dependency list (like requirements.txt in Python), sort dependencies.
- [ ] Warn users about abandoned dependencies with no maintenance
      for a long time and suggest equivalent drop-in replacements.

## Security

- [ ] Follow the principle of least privilege.
- [ ] Avoid using deprecated, obsolete, or insecure libraries,
      frameworks, or APIs.
- [ ] When handling sensitive data (like passwords, API keys, personal data),
      follow best practices for data protection and privacy.
- [ ] Avoid hardcoding sensitive information (like passwords, API keys)
      directly in the codebase.
- [ ] Validate and sanitize all user inputs to prevent security vulnerabilities
      such as SQL injection, cross-site scripting (XSS), and buffer overflows.
- [ ] Regularly update dependencies to their latest secure versions.
- [ ] When suggesting code that involves cryptography,
      use strong and well-established algorithms and key sizes.
- [ ] When dealing with authentication and authorization,
      follow best practices and standards like OAuth2, OpenID Connect, etc.
- [ ] Avoid using eval() and similar functions that execute arbitrary code,
      unless absolutely necessary and safe.
- [ ] Avoid the deserialization of untrusted data (CWE-502).
  - [ ] In Python, avoid using `pickle` module for
        serialization/deserialization.
- [ ] When handling files and paths, be careful of path traversal vulnerabilities
      like CWE-22.

## API

- [ ] The overall architecture, code, and API endpoints should follow the latest
      version of OpenAPI specification at <https://spec.openapis.org/oas/>
- [ ] API endpoints must use proper HTTP return codes.
- [ ] Follow web best practices as recommended by OpenAPI, IETF, W3C, etc.

## Git

- [ ] Follow these guidelines for writing a good commit message:
  - How to Write a Git Commit Message
    <https://chris.beams.io/posts/git-commit/>
  - Commit Verbs 101: why I like to use this and why you should also like it.
    <https://chris.beams.io/posts/git-commit/>

## Python

- [ ] Maintain source code readability.
- [ ] Use Idiomatic Python.
- [ ] All configurations should be in one place, the `pyproject.toml`,
      when possible. Use modern TOML syntax when is expressive enough.
- [ ] Defensive coding: always check for None/empty and handle exceptions
      when dealing with external inputs, like function arguments,
      file I/O, network I/O, etc.
- [ ] Complete type annotations for function, method, class, and variable,
      as much as possible.
  - [ ] Follow best practices and standard Python type hint patterns.
  - [ ] Use mypy as an assistant.
    - [ ] mypy is in "dev" optional dependency.
    - [ ] Sometimes mypy may report errors wrongly due to cache issues.
          Try to reset the cache if unexpected errors occured.
  - [ ] Use pyright, pyrefly, and pytype for second opinions.
  - [ ] When insert typing imports, put it in appropriate location and order.
        Use "if TYPE_CHECKING import" block when possible.
  - [ ] Minimize the use of `Any`. Try to find sources for type information
        of external libraries:
    - [ ] Check if type stub is available and install it.
    - [ ] Check if source code is available and analyze it for correct types.
          Open source library tend to have source code available on the
          internet. For example, at GitHub, GitLab, Codeberg.
          Try to find the source code repo from metadata in PyPI/pip.
  - [ ] Recheck necessity of casting.
  - [ ] Recheck necessity of `# noqa:` and `# type: ignore`.
  - [ ] Recheck docstring and documentation consistency with the code;
        They should match the updated type hints.
  - [ ] In docstring, use full qualified name for non-standard library types.
        For example, `numpy.ndarray` instead of `ndarray`;
        `pandas.DataFrame` instead of `pd.DataFrame`.
        So the user can know exactly which module the data type comes from.
- [ ] Try to achieve type completeness, according to
      <https://typing.python.org/en/latest/guides/libraries.html#type-completeness>.
      Also refer to Python type specification at
      <https://typing.python.org/en/latest/spec/>.
- [ ] `requires-python` in pyproject.toml should reflect the minimum
      Python version supported by the project.
- [ ] Do not introduce syntax or features that are not supported
      by the specified minimum Python version,
      unless it is supported via `__future__` imports.
- [ ] Do not use `A | B` union type syntax anywhere if minimum Python version is
      below 3.10.
- [ ] Make sure that the type annotations can be properly used by
      runtime type inspection tools, documentation generators, and static
      analysis tools. For example, `typing.get_type_hints()` and
      `inspect` should work properly.
- [ ] Do not allow the use of assert in production code
      (it is only allowed for testing and debugging).
- [ ] Do not use mutable default arguments in function/method definitions.
- [ ] Do not use wildcard imports (from module import *).
- [ ] When reordering the imports, be careful not to (re-)introduce circular
      import. Read comments near imports to get more information.
- [ ] Remove unused imports.
- [ ] Remove any trailing whitespace in the Python file.
- [ ] Make the package zip-safe if possible.
- [ ] Be mindful about choice of data structures.
      Prefer built-in data structures like list, dict, set, and tuple
      unless there is a specific need for specialized data structures.
      If specialized data structures are needed, consider using
      appropriate collection types from `collections` and
      `collections.abc` modules.
      Use the most appropriate data structure for the specific use case
      to optimize performance and memory usage.
- [ ] Recheck formatting with Ruff.
- [ ] Whem do packaging, the package metadata should follow
      the Core metadata specifications
      <https://packaging.python.org/en/latest/specifications/core-metadata/>.

## Python type completeness

The following are best practice recommendations for how to
define “type complete”:

- [ ] Classes:
  - [ ] All class variables, instance variables, and methods that
        are “visible” (not overridden) are annotated and refer to
        known types
  - [ ] If a class is a subclass of a generic class, type arguments
        are provided for each generic type parameter, and these type
        arguments are known types
- [ ] Functions and Methods:
  - [ ] All input parameters have type annotations that refer to
        known types
  - [ ] The return parameter is annotated and refers to a known type
  - [ ] The result of applying one or more decorators results in
        a known type
- [ ] Type Aliases:
  - [ ] All of the types referenced by the type alias are known
- [ ] Variables:
  - [ ] All variables have type annotations that refer to known types

Type annotations can be omitted in a few specific cases
where the type is obvious from the context:

- Constants that are assigned simple literal values
  (e.g. `RED = '#F00'` or `MAX_TIMEOUT = 50` or
  `room_temperature: Final = 20`).
  A constant is a symbol that is assigned only once and is either
  annotated with `Final` or is named in all-caps.
  A constant that is not assigned a simple literal value requires
  explicit annotations, preferably with a Final annotation
  (e.g. `WOODWINDS: Final[list[str]] = ['Oboe', 'Bassoon']`).
- Enum values within an `Enum` class do not require annotations
  because they take on the type of the `Enum` class.
- Type aliases do not require annotations.
  A type alias is a symbol that is defined at a module level
  with a single assignment where the assigned value is an
  instantiable type, as opposed to a class instance
  (e.g. `Foo = Callable[[Literal["a", "b"]], int | str]` or
  `Bar = MyGenericClass[int] | None`).
- The “self” parameter in an instance method and the “cls”
  parameter in a class method do not require an explicit annotation.
- The return type for an `__init__` method does not need
  to be specified, since it is always `None`.
- The following module-level symbols do not require type annotations:
  `__all__`, `__author__`, `__copyright__`, `__email__`,
  `__license__`, `__title__`, `__uri__`, `__version__`.
- The following class-level symbols do not require type annotations:
  `__class__`, `__dict__`, `__doc__`, `__module__`, `__slots__`.

## JSON

- [ ] When serialize to JSON, always enclose decimal values
      (for example, xs:decimal) in quotes to guarantee correct type
      interpretation and preserve precision.
- [ ] Make sure JSON is valid and well-formatted.

## Markdown

- [ ] When including metadata in Markdown file,
      put them as YAML between triple-dashed lines,
      as used by Hugo and Jekyll front matter.
- [ ] Be strict on the Markdown formatting.
      Be mindful that what works on GitHub may not work on MkDocs, for example.
      Try to keep with the standard Markdown.
- [ ] Use Markdownlint to detect and fix malformatted.

## Diagram

- [ ] When draw the diagram in ASCII/text, recheck if all the lines are well
      aligned.
      Count the characters and adjust the spaces so the lines align well.

## HTML

- [ ] Make sure HTML is valid and well-formatted.
- [ ] Make sure there is no trailing whitespace in the HTML file.
- [ ] Be conscious about accessibility. Consider to follow W3C web
      accessibility recommendations when possible.
- [ ] Use sensible and concise element IDs and names that allow code
      readability, name grouping also helps.

## CSS

- [ ] Make sure there is no unused styles.
- [ ] Use sensible and concise element IDs and names that allow code
      readability, name grouping also helps.

## Version

- [ ] When suggest dependencies, recheck the version; if the version exists,
      or if the version is compatible with the system or other dependencies.
- [ ] Prefer a Semantic Version when applicable.
