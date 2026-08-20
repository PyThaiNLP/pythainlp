# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for PyTorch-based functionalities.

Test functions that require PyTorch and its ecosystem dependencies:
- torch
- transformers (when using PyTorch backend)
- attacut
- thai-nner
- wtpsplit

These tests are NOT run in automated CI workflows due to:
- Very large dependencies (~2-3 GB for torch)
- Potential version conflicts with other frameworks
- Long installation time

These tests are kept for manual testing and may be run in separate CI
workflows dedicated to PyTorch-based features.
"""

from tests._noauto_loader import make_load_tests

test_packages: list[str] = [
    "tests.noauto_torch.testn_augment_torch",
    "tests.noauto_torch.testn_lm_torch",
    "tests.noauto_torch.testn_parse_torch",
    "tests.noauto_torch.testn_spell_torch",
    "tests.noauto_torch.testn_summarize_torch",
    "tests.noauto_torch.testn_tag_torch",
    "tests.noauto_torch.testn_tokenize_torch",
    "tests.noauto_torch.testn_transliterate_torch",
]

load_tests = make_load_tests(test_packages)

if __name__ == "__main__":
    from unittest import main

    main()
