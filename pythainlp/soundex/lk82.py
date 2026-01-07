# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex - LK82 system

Original paper:
Vichit Lorchirachoonkul. 1982. A Thai soundex
system. Information Processing & Management,
18(5):243–255.
https://doi.org/10.1016/0306-4573(82)90003-6

Python implementation:
Improved implementation contributed to PyThaiNLP project
based on the original paper's algorithm.
"""

# Table 2: Initial Consonant Map
# Maps initial consonants to their representative Soundex letter.
_INITIAL_MAP = {
    'ก': 'ก', 'ข': 'ก', 'ฃ': 'ก', 'ค': 'ก', 'ฅ': 'ก', 'ฆ': 'ก',
    'ง': 'ง',
    'จ': 'จ', 'ฉ': 'จ', 'ช': 'จ', 'ฌ': 'จ',
    'ซ': 'ซ', 'ศ': 'ส', 'ษ': 'ส', 'ส': 'ส',
    'ญ': 'ย', 'ย': 'ย',
    'ฎ': 'ด', 'ด': 'ด', 'ต': 'ต', 'ฏ': 'ต',
    'ฐ': 'ท', 'ฑ': 'ท', 'ฒ': 'ท', 'ถ': 'ท', 'ท': 'ท', 'ธ': 'ท',
    'ณ': 'น', 'น': 'น',
    'บ': 'บ', 'ป': 'ป',
    'ผ': 'พ', 'พ': 'พ', 'ภ': 'พ',
    'ฝ': 'ฟ', 'ฟ': 'ฟ',
    'ม': 'ม',
    'ร': 'ร', 'ฤ': 'ร',
    'ล': 'ล', 'ฦ': 'ล', 'ฬ': 'ล',
    'ว': 'ว',
    'ห': 'ห', 'ฮ': 'ห',
    'อ': 'อ'
}

# Table 3: Final Consonant/Vowel Hex Codes
_CODE_MAP = {
    # Group 1 (Guttural) -> 1
    'ก': '1', 'ข': '1', 'ฃ': '1', 'ค': '1', 'ฅ': '1', 'ฆ': '1',
    # Group 2 (Velar Nasal) -> 2
    'ง': '2',
    # Group 3 (Dental/Sibilant) -> 3
    'จ': '3', 'ฉ': '3', 'ช': '3', 'ฌ': '3',
    'ฎ': '3', 'ฏ': '3', 'ฐ': '3', 'ฑ': '3', 'ฒ': '3',
    'ด': '3', 'ต': '3', 'ถ': '3', 'ท': '3', 'ธ': '3',
    'ศ': '3', 'ษ': '3', 'ส': '3', 'ซ': '3',
    # Group 4 (Nasals/Liquids) -> 4
    'น': '4', 'ณ': '4', 'ล': '4', 'ฬ': '4', 'ฤ': '4', 'ฦ': '4',
    'ญ': '4',
    # Group 5 (Labials) -> 5
    'บ': '5', 'ป': '5', 'ผ': '5', 'ฝ': '5', 'พ': '5', 'ฟ': '5', 'ภ': '5',
    # Group 6 (Labial Nasal) -> 6
    'ม': '6',
    # Group 7 (Semivowels) -> 7
    'ย': '7', 'ว': '7', 'ไ': '7', 'ใ': '7', 'ำ': '7',
    # Group 8 (Glottal) -> 8
    'ห': '8', 'ฮ': '8',
    # Vowels/Separators
    'า': '9', 'ๅ': '9',  # Sara A -> 9
    'เ': 'B', 'แ': 'B',  # Leading vowels -> B
    'โ': 'C',            # Sara O -> C
    'ุ': 'E', 'ู': 'E',  # Sara U -> E
    'อ': 'F'
}

# Separators that reset the duplication check
# Note: 'า' and 'ำ' also produce codes in addition to being separators
_SEPARATORS = {'ะ', 'ั', 'า', 'ำ'}

# Characters to ignore completely
_IGNORE_CHARS = {'ๆ', 'ิ', 'ี', 'ํ', 'ื', 'ึ'}
_TONE_MARKS = {'่', '้', '๊', '๋'}


def lk82(text: str) -> str:
    """
    This function converts Thai text into phonetic code with the
    Thai soundex algorithm named **LK82** [#lk82]_.

    :param str text: Thai word

    :return: LK82 soundex of the given Thai word
    :rtype: str

    :Example:
    ::

        from pythainlp.soundex import lk82

        lk82("ลัก")
        # output: 'ร1000'

        lk82("รัก")
        # output: 'ร1000'

        lk82("รักษ์")
        # output: 'ร1000'

        lk82("บูรณการ")
        # output: 'บE419'

        lk82("ปัจจุบัน")
        # output: 'ป3E54'
    """
    if not text or not isinstance(text, str):
        return ""

    chars = list(text.strip())

    if not chars:
        return ""

    # 1. Rule 6: Swap Leading Vowels (เ, แ, โ, ไ, ใ)
    leading_vowels = {'เ', 'แ', 'โ', 'ไ', 'ใ'}
    if len(chars) > 1 and chars[0] in leading_vowels:
        chars[0], chars[1] = chars[1], chars[0]

    soundex = ""
    last_metric_code = ""
    start_idx = 0
    initial_found = False

    # 2. Identify Initial Consonant
    for i, char in enumerate(chars):
        if char in _TONE_MARKS or char in _IGNORE_CHARS:
            continue
        if char in _INITIAL_MAP:
            soundex += _INITIAL_MAP[char]
            # Map initial to its code for duplicate checking of the next char
            if char in _CODE_MAP:
                last_metric_code = _CODE_MAP[char]
            start_idx = i + 1
            initial_found = True
            break

    if not initial_found:
        return text

    # 3. Process Remaining Characters
    digit_count = 0
    prev_was_digit = False  # Track if previous char produced a digit (or was a separator)
    prev_char = None  # Track previous character for special vowel handling
    has_content = False  # Track if we have any content besides the initial

    for i in range(start_idx, len(chars)):
        char = chars[i]

        # Skip ignored characters and tones
        if char in _TONE_MARKS or char in _IGNORE_CHARS:
            continue

        # Skip Karan (Silencer) and the character it marks
        if char == '์':
            continue
        if i + 1 < len(chars) and chars[i + 1] == '์':
            continue

        # Rule 11: Ignore Semivowels (ร, ว, ย) if they follow a digit/separator
        # They are kept only if they immediately follow the Initial Consonant (Initial Cluster)
        if char in ['ร', 'ว', 'ย', 'ฤ', 'ฦ']:
            if prev_was_digit:
                continue

        # Handle Separators (Reset duplicate check)
        if char in _SEPARATORS:
            # Separators silence following semivowels
            prev_was_digit = True

            # Check if separator also produces a code
            if char in _CODE_MAP:
                current_code = _CODE_MAP[char]
                # Rule 13: Check duplicate before resetting
                if current_code != last_metric_code:
                    soundex += current_code
                    digit_count += 1
                    has_content = True
            
            # Reset last_metric_code after processing
            last_metric_code = "SEP"
            continue

        # Special handling for 'ุ' (Sara U): Skip if it follows 'ต' or 'ธ'
        # This maintains compatibility with the original implementation
        if char == 'ุ' and prev_char in ['ต', 'ธ']:
            continue

        # Map Code
        current_code = _CODE_MAP.get(char)

        if current_code:
            # Rule 13: Duplicate Check
            if current_code != last_metric_code:
                soundex += current_code
                last_metric_code = current_code

                prev_was_digit = True
                has_content = True

                digit_count += 1

        prev_char = char

        if digit_count >= 4:
            break

    # Special case: if only initial consonant with no other content (e.g., "น์"),
    # return empty string for compatibility
    if not has_content and len(soundex) == 1:
        return ""

    # 4. Pad with Zeros
    while digit_count < 4:
        soundex += "0"
        digit_count += 1

    return soundex
