# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Calendar constants shared by the date utilities."""

from __future__ import annotations

# Buddhist Era (BE) year = Anno Domini (AD) year + 543
_BE_AD_OFFSET: int = 543

# Offset of each era from the Buddhist Era: era year = BE year + offset
_ERA_OFFSETS_FROM_BE: dict[str, int] = {
    "be": 0,
    "ad": -_BE_AD_OFFSET,
    "re": -2324,  # Rattanakosin era
    "ah": -1122,  # Anno Hejira
}
