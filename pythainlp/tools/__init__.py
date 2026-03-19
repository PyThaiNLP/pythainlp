# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
__all__: list[str] = [
    "PYTHAINLP_DEFAULT_DATA_DIR",
    "get_full_data_path",
    "get_pythainlp_data_path",
    "get_pythainlp_path",
    "is_offline_mode",
    "is_read_only_mode",
    "is_unsafe_pickle_allowed",
    "safe_path_join",
    "safe_print",
    "warn_deprecation",
]

from pythainlp.tools.core import safe_print, warn_deprecation
from pythainlp.tools.path import (
    PYTHAINLP_DEFAULT_DATA_DIR,
    get_full_data_path,
    get_pythainlp_data_path,
    get_pythainlp_path,
    is_offline_mode,
    is_read_only_mode,
    is_unsafe_pickle_allowed,
    safe_path_join,
)
