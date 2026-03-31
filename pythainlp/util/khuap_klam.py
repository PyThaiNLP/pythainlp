# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai consonant cluster (Kham Khuap Klam) checker."""

from __future__ import annotations

import re
from typing import Optional

# Regex for true consonant clusters (คำควบกล้ำแท้):
# initial consonants ก ข ค ต ป ผ พ ฟ บ followed by ร ล ว
_TRUE_CLUSTER_RE = re.compile(r"^[กขคตปผพฟบ][รลว]")

# Regex for false consonant clusters (คำควบกล้ำไม่แท้):
# written forms that look like clusters but are not pronounced as such
_FALSE_CLUSTER_RE = re.compile(r"^(ทร|จร|ศร|สร|ซร)")

# Leading vowels that appear before the initial consonant in written Thai
_LEAD_VOWEL_RE = re.compile(r"^[เแโใไ]+")


def _strip_lead_vowels(text: str) -> str:
    """Remove leading vowels (เ แ โ ใ ไ) from the start of *text*."""
    return _LEAD_VOWEL_RE.sub("", text)


def check_khuap_klam(word: str) -> Optional[bool]:
    """Check whether a Thai word is a consonant cluster (Kham Khuap Klam).

    :param str word: Thai word to check.
    :return: ``True`` if the word is a *true* consonant cluster
        (คำควบกล้ำแท้), ``False`` if it is a *false* consonant cluster
        (คำควบกล้ำไม่แท้), or ``None`` if it is not a consonant cluster.
    :rtype: Optional[bool]

    :Example:

        >>> from pythainlp.util import check_khuap_klam  # doctest: +SKIP

        >>> # True consonant clusters (คำควบกล้ำแท้)
        >>> print(check_khuap_klam("กราบ"))  # True  # doctest: +SKIP
        >>> print(check_khuap_klam("ปลา"))  # True  # doctest: +SKIP
        >>> print(check_khuap_klam("เพราะ"))  # True  # doctest: +SKIP
        >>> print(check_khuap_klam("ตรง"))  # True  # doctest: +SKIP

        >>> # False consonant clusters (คำควบกล้ำไม่แท้)
        >>> print(check_khuap_klam("จริง"))  # False  # doctest: +SKIP
        >>> print(check_khuap_klam("ทราย"))  # False  # doctest: +SKIP
        >>> print(check_khuap_klam("เศร้า"))  # False  # doctest: +SKIP

        >>> # Not a consonant cluster
        >>> print(check_khuap_klam("แม่"))  # None  # doctest: +SKIP
        >>> print(check_khuap_klam("ตา"))  # None  # doctest: +SKIP
    """
    if not word:
        return None

    from ..transliterate import pronunciate

    # Convert to pronunciation; remove sub-consonant marker (พินทุ ฺ)
    reading = pronunciate(word, engine="w2p").replace("\u0e3a", "")

    # Use only the first syllable of the reading
    first_syll_reading = reading.split("-")[0]

    written_core = _strip_lead_vowels(word)
    reading_core = _strip_lead_vowels(first_syll_reading)

    is_true_sound = bool(_TRUE_CLUSTER_RE.match(reading_core))
    is_false_form = bool(_FALSE_CLUSTER_RE.match(written_core))

    if is_true_sound:
        return True
    if is_false_form:
        return False
    return None
