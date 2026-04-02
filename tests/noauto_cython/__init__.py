# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for Cython-compiled package functionalities.

Test functions that require packages that need Cython compilation:
- phunspell (requires Cython and hunspell C library)

These tests are NOT run in automated CI workflows due to:
- Compilation requirements (Cython, C compiler)
- System library dependencies
- Platform-specific build issues

These tests are kept for manual testing and may be run in separate CI
workflows with appropriate build environments.
"""

from tests._noauto_loader import make_load_tests

test_packages: list[str] = [
    "tests.noauto_cython.testn_spell_cython",
    "tests.noauto_cython.testn_fast_functions",
]

load_tests = make_load_tests(test_packages)

if __name__ == "__main__":
    from unittest import main

    main()
