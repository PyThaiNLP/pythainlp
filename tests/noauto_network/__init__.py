# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for network-dependent functionalities.

Test functions that require network access:
- HuggingFace Hub downloads
- Model downloads from remote servers
- API calls to external services

These tests are NOT run in automated CI workflows due to:
- Network dependency
- Potential for large downloads
- External service availability
- Rate limiting concerns

These tests are kept for manual testing and may be run in environments
with appropriate network access and caching.
"""

from tests._noauto_loader import make_load_tests

test_packages: list[str] = [
    "tests.noauto_network.testn_spell_network",
]

load_tests = make_load_tests(test_packages)

if __name__ == "__main__":
    from unittest import main

    main()
