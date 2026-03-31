# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

THAI_MORSE_CODE: dict[str, str] = {
    "ก": "--.",
    "ข": "-.-.",
    "ค": "-.-",
    "ฆ": "-.-",
    "ง": "-.--.",
    "จ": "-..-.",
    "ฉ": "----",
    "ช": "-..-",
    "ฌ": "-..-",
    "ซ": "--..",
    "ญ": ".---",
    "ด": "-..",
    "ถ": "-.-..",
    "ฐ": "-.-..",
    "ฑ": "-..--",
    "ฒ": "-..--",
    "ท": "-..--",
    "ธ": "-..--",
    "ณ": "-.",
    "น": "-.",
    "บ": "-...",
    "ป": ".--.",
    "ผ": "--.-",
    "ฝ": "-.-.-",
    "พ": ".--..",
    "ภ": ".--..",
    "ฟ": "..-.",
    "ม": "--",
    "ย": "-.--",
    "ร": ".-.",
    "ล": ".-..",
    "ฬ": ".-..",
    "ว": ".--",
    "ศ": "...",
    "ษ": "...",
    "ส": "...",
    "ห": "....",
    "ฮ": "--.--",
    "ฎ": "-..",
    "ต": "-",
    "ฏ": "-",
    "ฤ": ".-.--",
    "่": "..-",
    "้": "...-",
    "๊": "--...",
    "๋": ".-.-.",
    "ั": ".--.-",
    "็": "---..",
    "์": "--..-",
    "ั้": ".---.",
    "ฯ": "--.-.",
    "ฯลฯ": "---.-",
    "ๆ": "---.-",
    "ะ": ".-...",
    "า": ".-",
    "ิ": "..-..",
    "ี": "..",
    "ึ": "..--.",
    "ื": "..--",
    "ุ": "..-.-",
    "ู": "---.",
    "เ": ".",
    "แ": ".-.-",
    "โ": "---",
    "ไ": ".-..-",
    "ใ": ".-..-",
    "ำ": "...-.",
    "อ": "-...-",
}

ENGLISH_MORSE_CODE: dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    ",": "--..--",
    "1": ".----",
    ".": ".-.-.-",
    "2": "..---",
    "?": "..--..",
    "3": "...--",
    ";": "-.-.-.",
    "4": "....-",
    ":": "---...",
    "5": ".....",
    "'": ".----.",
    "6": "-....",
    "-": "-....-",
    "7": "--...",
    "/": "-..-.",
    "8": "---..",
    "(": "-.--.-",
}

decodingeng: dict[str, str] = {}
key: str
val: str
for key, val in ENGLISH_MORSE_CODE.items():
    decodingeng[val] = key

decodingthai: dict[str, str] = {}
for key, val in THAI_MORSE_CODE.items():
    decodingthai[val.replace(" ", "")] = key

for key, val in THAI_MORSE_CODE.items():
    THAI_MORSE_CODE[key] = val.replace(" ", "")


def morse_encode(text: str, lang: str = "th") -> str:
    """Convert text to Morse code (support Thai and English)

    :param str text: Text
    :param str lang: Language Code (*th* is Thai and *en* is English)
    :return: Morse code
    :rtype: str

    :Example:

        >>> from pythainlp.util.morse import morse_encode
        >>> morse_encode("แมว", lang="th")
        '.-.- -- .--'
        >>> morse_encode("cat", lang="en")
        '-.-. .- -'
    """
    if lang == "th":  # Thai
        return " ".join(
            THAI_MORSE_CODE.get(char, " ") for char in text.upper()
        )
    elif lang == "en":  # English
        return " ".join(
            ENGLISH_MORSE_CODE.get(char, " ") for char in text.upper()
        )
    else:
        raise NotImplementedError(f"This function doesn't support {lang}.")


def morse_decode(morse_text: str, lang: str = "th") -> str:
    """Convert Morse code to text.

    Thai decoding may produce incorrect characters
    that can be fixed with a spell corrector.

    :param str morse_text: Morse code
    :param str lang: language code (``'th'`` for Thai, ``'en'`` for English)
    :return: decoded text
    :rtype: str

    :Example:

        >>> from pythainlp.util.morse import morse_decode
        >>> morse_decode(".-.- -- .--", lang="th")
        'แมว'
        >>> morse_decode("-.-. .- -", lang="en")
        'CAT'
    """
    if lang == "th":
        ans = "".join(
            decodingthai.get(code, "") for code in morse_text.split(" ")
        )
        return "".join(ans.split())
    elif lang == "en":
        ans = "".join(
            decodingeng.get(code, " ") for code in morse_text.split(" ")
        )
        return " ".join(ans.split())
    else:
        raise NotImplementedError(f"This function doesn't support {lang}.")
