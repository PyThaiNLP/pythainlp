# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""PyThaiNLP Coreference Resolution"""

__all__: list[str] = ["CorefResult", "coreference_resolution"]

from pythainlp.coref._fastcoref import CorefResult
from pythainlp.coref.core import coreference_resolution
