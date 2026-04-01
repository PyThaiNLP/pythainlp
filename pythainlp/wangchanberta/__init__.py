# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Named entity recognition using WangchanBERTa."""
__all__: list[str] = [
    "NamedEntityRecognition",
    "ThaiNameTagger",
    "segment",
]

from pythainlp.wangchanberta.core import (
    NamedEntityRecognition,
    ThaiNameTagger,
    segment,
)
