# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Text classification."""

__all__: list[str] = [
    "GzipModel",
    "Laya",
    "LayaModel",
]

from pythainlp.classify.laya import Laya, LayaModel
from pythainlp.classify.param_free import GzipModel
