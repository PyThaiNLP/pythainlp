# -*- coding: utf-8 -*-
"""
Check if it is Thai text
"""
import string

_DEFAULT_IGNORE_CHARS = string.whitespace + string.digits + string.punctuation


def isthaichar(ch: str) -> bool:
    """
    This function checks if the input character is a Thai character.

    :param str ch: input character

    :return: returns **True** if the input character is a Thai characttr,
             otherwise returns **False**
    :rtype: bool

    :Example:

        >>> from pythainlp.util import isthaichar
        >>>
        >>> isthaichar("ก") # THAI CHARACTER KO KAI
        True
        >>> isthaichar("๐") # THAI DIGIT ZERO
        True
        >>> isthaichar("๕") # THAI DIGIT FIVE
        True
        >>> isthaichar("฿") # THAI CURRENCY SYMBOL BAHT
        True
        >>> isthaichar("๏") # THAI CHARACTER FONGMAN
        True
        >>>
        >>> isthaichar("A") # LATIN CAPITAL LETTER A
        False
        >>> isthaichar(",") # COMMA
        False
        >>> isthaichar(".") # FULL STOP
        False
    """
    ch_val = ord(ch)
    if ch_val >= 3584 and ch_val <= 3711:
        return True
    return False


def isthai(word: str, ignore_chars: str = ".") -> bool:
    """
    This function checks if all character in the input string
    are Thai character.

    :param str word: input text
    :param str ignore_chars: string characters to be ignored
                             (i.e. will be considered as Thai)

    :return: returns **True** if the input text all contains Thai characters,
             otherwise returns **False**
    :rtype: bool

    :Example:

        Check if all character is Thai character. By default,
        it ignores only full stop (".").

        >>> from pythainlp.util import isthai
        >>> isthai("กาลเวลา")
        True
        >>> isthai("กาลเวลา.")
        True
        >>> isthai("กาลเวลา,")
        False
        >>> isthai("กาลเวลา ")
        False
        >>> isthai("กาลเวลา-")
        False
        >>> isthai("กาลเวลา3")
        False
        >>> isthai("กาลเวลาDw")
        False

        Explicitly ignore digits, whitespace, and the following characters
        ("-", ".", "$", ",").

        >>> from pythainlp.util import isthai
        >>> isthai("กาลเวลา, การเวลา-ก,  3.75$", \\
            ignore_chars="1234567890.-,$ ")
        True

    """
    if not ignore_chars:
        ignore_chars = ""

    for ch in word:
        if ch not in ignore_chars and not isthaichar(ch):
            return False
    return True


def countthai(text: str, ignore_chars: str = _DEFAULT_IGNORE_CHARS) -> float:
    """
    This function calculates percentage of Thai characters in the text
    with an option to ignored some characters.

    :param str text: input text
    :param str ignore_chars: string of characters to ignore from counting.
                             By default, the ignored characters are whitespace,
                             newline, digits, and punctuation.

    :return: percentage of Thai characters in the text
    :rtype: float

    :Example:

        Find the percentage of Thai characters in the textt with default
        ignored characters set (whitespace, newline character,
        punctuation and digits).

        >>> from pythainlp.util import countthai
        >>>
        >>> countthai("ดอนัลด์ จอห์น ทรัมป์ English: Donald John Trump")
        45.0
        >>>
        >>> countthai("ดอนัลด์ จอห์น ทรัมป์ (English: Donald John Trump)")
        45.0
        >>>
        >>> countthai("(English: Donald John Trump)")
        0.0

        Find the percentage of Thai characters in the text while ignoring
        only punctuation but not whitespace, newline character and digits.

        >>> import string
        >>> from pythainlp.util import countthai
        >>>
        >>> string.punctuation
        !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
        >>>
        >>> countthai("ดอนัลด์ จอห์น ทรัมป์ English: Donald John Trump", \\
            ignore_chars=string.punctuation)
        39.130434782608695
        >>>
        >>> countthai("ดอนัลด์ จอห์น ทรัมป์ (English: Donald John Trump)", \\
            ignore_chars=string.punctuation)
        39.130434782608695
        >>>
        >>> countthai("(English: Donald John Trump)", \\
            ignore_chars=string.punctuation)
        0.0
    """
    if not text or not isinstance(text, str):
        return 0

    if not ignore_chars:
        ignore_chars = ""

    num_thai = 0
    num_ignore = 0

    for ch in text:
        if ch in ignore_chars:
            num_ignore += 1
        elif isthaichar(ch):
            num_thai += 1

    num_count = len(text) - num_ignore

    return (num_thai / num_count) * 100
