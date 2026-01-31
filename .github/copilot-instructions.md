# Instructions

## Project contribution guidelines

- [ ] Follow the project's established coding style and conventions.
- [ ] Run Ruff and fix errors before committing code.
  - [ ] New code should be written to pass all Ruff checks.
  - [ ] McCabe complexity should be kept low; refactor the new code
        that exceeds 10.
  - [ ] Existing code should be gradually improved to pass Ruff checks
        when making changes.
- [ ] Write clear and concise commit messages that accurately describe
      the changes made.
- [ ] For significant changes, update the CHANGELOG.md file
      to document the changes.
  - [ ] Follow "Keep a Changelog" principles
        https://keepachangelog.com/en/1.0.0/
  - [ ] Use semantic versioning for version numbers
        https://semver.org/
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
      https://www.w3.org/TR/cooluris/
- [ ] Consult Schema.org vocabularies when deciding about names.
- [ ] Consult "Style Guidelines for Naming and Labeling Ontologies in the
      Multilingual Web" https://www.researchgate.net/publication/277224472

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
      See https://spdx.github.io/spdx-spec/v2.3/file-information/
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
      version of OpenAPI specification at https://spec.openapis.org/oas/
- [ ] API endpoints must use proper HTTP return codes.
- [ ] Follow web best practices as recommended by OpenAPI, IETF, W3C, etc.

## Python

- [ ] Defensive coding: always check for None/empty and handle exceptions
      when dealing with external inputs, like function arguments,
      file I/O, network I/O, etc.
- [ ] Use type hints for function/method signatures
      and variable declarations as much as possible.
- [ ] requires-python in pyproject.toml should reflect the minimum
      Python version supported by the project.
- [ ] Do not introduce syntax or features that are not supported
      by the specified minimum Python version,
      unless it is supported via `__future__` imports.
  - [ ] Do not use | union type syntax if minimum Python version is
        below 3.10.  
- [ ] Make sure that the module/class/function/object can be properly used by
      runtime type inspection tools, documentation generators, and static
      analysis tools.
      For example, typing.get_type_hints() should work properly.
- [ ] Do not use mutable default arguments in function/method definitions.
- [ ] Do not use wildcard imports (from module import *).
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
