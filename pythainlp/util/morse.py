# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

THAI_MORSE_CODE = {
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

ENGLISH_MORSE_CODE = {
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

decodingeng = {}
for key, val in ENGLISH_MORSE_CODE.items():
    decodingeng[val] = key

decodingthai = {}
for key, val in THAI_MORSE_CODE.items():
    decodingthai[val.replace(" ", "")] = key

for key, val in THAI_MORSE_CODE.items():
    THAI_MORSE_CODE[key] = val.replace(" ", "")


def morse_encode(text: str, lang: str = "th") -> str:
    """
    Convert text to Morse code (support Thai and English)

    :param str text: Text
    :param str lang: Language Code (*th* is Thai and *en* is English)
    :return: Morse code
    :rtype: str

    :Example:
    ::

        from pythainlp.util.morse import morse_encode
        print(morse_encode("แมว", lang="th"))
        # output: .-.- -- .--

        print(morse_encode("cat", lang="en"))
        # output: -.-. .- -
    """
    if lang == "th":  # Thai
        return " ".join(
            map(lambda x, g=THAI_MORSE_CODE.get: g(x, " "), text.upper())
        )
    elif lang == "en":  # English
        return " ".join(
            map(lambda x, g=ENGLISH_MORSE_CODE.get: g(x, " "), text.upper())
        )
    else:
        raise NotImplementedError(f"This function doesn't support {lang}.")


def morse_decode(morse_text: str, lang: str = "th") -> str:
    """
    Simple Convert Morse code to text

    Thai still have some wrong character problem that\
        can fix by spell corrector.

    :param str morse_text: Morse code
    :param str lang: Language Code (*th* is Thai and *en* is English)
    :return: Text
    :rtype: str

    :Example:
    ::

        from pythainlp.util.morse import morse_decode
        print(morse_decode(".-.- -- .--", lang="th"))
        # output: แมว

        print(morse_decode("-.-. .- -", lang="en"))
        # output: CAT
    """
    if lang == "th":
        ans = "".join(
            map(lambda x, g=decodingthai.get: g(x, ""), morse_text.split(" "))
        )
        return "".join(ans.split())
    elif lang == "en":
        ans = "".join(
            map(lambda x, g=decodingeng.get: g(x, " "), morse_text.split(" "))
        )
        return " ".join(ans.split())
    else:
        raise NotImplementedError(f"This function doesn't support {lang}.")
