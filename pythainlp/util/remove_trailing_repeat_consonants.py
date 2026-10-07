# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Removal of repeated consonants at the end of words."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

from pythainlp import thai_consonants as consonants
from pythainlp.corpus import thai_words

# used by remove_trailing_repeat_consonants()
# contains all words that has repeating consonants at the end
# for each consonant
# when dictionary updated, this should be updated too
# key: consonant
# value: list of words that has repeating consonants at the end
last_consonants_repeaters: dict[str, list[str]] = {}


def remove_trailing_repeat_consonants(
    text: str,
    custom_dict: Iterable[str] = [],
    has_dictionary_updated: bool = True,
) -> str:
    """
    Remove repeating consonants at the end of words in text.

    Remove the repeating consonants before a whitespace, a new line, or
    the end of text, so that the last word matches a word in the
    dictionary. If there is no match, reduce the repeating consonants
    to one. If there are several matches, use the longest word.
    Since this function uses a dictionary, the result may differ
    depending on the dictionary used.
    Use :func:`pythainlp.util.normalize` for better results.

    :param str text: text to be processed
    :param Iterable[str] custom_dict: dictionary to check the last word.
        If empty, :func:`pythainlp.corpus.thai_words` is used
    :param bool has_dictionary_updated: set to True if the dictionary
        is updated or used for the first time in the kernel,
        otherwise set to False to save time
    :return: text without repeating Thai consonants
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_trailing_repeat_consonants
        >>> from pythainlp.util import dict_trie
        >>> # use default dictionary (pythainlp.corpus.thai_words())
        >>> remove_trailing_repeat_consonants("เริ่ดดดดดดดด")
        'เริ่ด'
        >>> # "อืมมม" is in the default dictionary
        >>> remove_trailing_repeat_consonants("อืมมมมมมมมมมมมมมม")
        'อืมมม'
        >>> # use custom dictionary
        >>> custom_dict = dict_trie(["อืมมมมม"])
        >>> remove_trailing_repeat_consonants("อืมมมมมมมมมมมมมมม", custom_dict)
        'อืมมมมม'
        >>> remove_trailing_repeat_consonants("เริ่ดดด คุณณณ ความลับบบบบ")
        'เริ่ด คุณ ความลับ'
    """
    # use default dictionary if not given
    if not custom_dict:
        custom_dict = thai_words()

    # update repeaters dictionary if not updated
    if has_dictionary_updated:
        _update_consonant_repeaters(custom_dict)

    # separate by newline
    modified_lines = []
    for line in text.split("\n"):
        segments = line.split(" ")

        for cnt, segment in enumerate(segments):
            segments[cnt] = _remove_repeat_trailing_consonants_from_segment(
                segment
            )

        # revert spaces
        modified_line = " ".join(segments)
        modified_lines.append(modified_line)

    # revert newlines
    modified_text = "\n".join(modified_lines)

    return modified_text


def _remove_repeat_trailing_consonants_from_segment(segment: str) -> str:
    """
    Remove repeating consonants at the end of a segment.

    Process only the end of the segment.
    Details are the same as :func:`remove_trailing_repeat_consonants`.

    :param str segment: segment of text
    :return: segment without repeating Thai consonants
    :rtype: str
    """
    # skip if the segment is not the target
    if not (
        # the segment is long enough
        (len(segment) > 1)
        # last is Thai consonant
        and (segment[-1] in consonants)
        # has repetition
        and (segment[-1] == segment[-2])
    ):
        # no need to process
        return segment

    # duplicating character
    dup = segment[-1]

    # find the words that has 2 or more duplication of
    # this character at the end.
    repeaters = last_consonants_repeaters[dup]

    # remove all of the last repeating character
    segment_head = _remove_all_last_consonants(segment, dup)

    # find the longest word that matches the segment
    longest_word, repetition = _find_longest_consonant_repeaters_match(
        segment_head, repeaters
    )

    if len(longest_word) > 0:
        # if there is a match, use it
        segment = segment_head + (dup * repetition)
    else:
        # if none found,
        # the chance is that the correct is one character,
        # or it's not in the dictionary.

        # make the repetition to once
        segment = segment_head + (dup * 1)

    return segment


def _remove_all_last_consonants(text: str, dup: str) -> str:
    """
    Remove repeating characters at the end of text.

    Return the text just before the repeating characters.

    :param str text: text to be processed
    :param str dup: repeating character to be removed
    :return: text without repeating characters at the end
    :rtype: str
    """
    removed = text
    while (len(removed) > 0) and (removed[-1] == dup):
        removed = removed[:-1]

    return removed


def _update_consonant_repeaters(custom_dict: Iterable[str]) -> None:
    """
    Update the dictionary of words with repeating consonants at the end.

    Search the dictionary for all words with more than one consonant
    repeating at the end, and store them in the global dictionary.

    :param Iterable[str] custom_dict: dictionary to search
    :rtype: None
    """
    # initialize dictionary
    for consonant in list(consonants):
        last_consonants_repeaters[consonant] = []

    # register
    for word in custom_dict:
        if _is_last_consonant_repeater(word):
            last_consonants_repeaters[word[-1]].append(word)

    return


def _is_last_consonant_repeater(word: str) -> bool:
    """
    Check if the word has repeating consonants at the end.

    Check whether a word has more than one repeating consonant at the end.

    :param str word: word to be checked
    :return: True if the word has repeating consonants at the end
    :rtype: bool
    """
    return (
        (len(word) > 1) and (word[-1] == word[-2]) and (word[-1] in consonants)
    )


def _find_longest_consonant_repeaters_match(
    segment_head: str, repeaters: list[str]
) -> tuple[str, int]:
    """
    Find the longest word that matches the segment.

    Find the longest word that matches the end of a segment.

    Search the list of repeaters. Return the word and the number of
    times its last character is repeated correctly.

    :param str segment_head: segment of text without its last repeating
        consonants
    :param list[str] repeaters: words with repeating consonants at the end
    :return: tuple of the word and the number of correct repetitions
        of its last character, or ``("", 0)`` if none is found
    :rtype: tuple[str, int]
    """
    longest_word = ""  # the longest word that matches the segment
    repetition = 0  # how much the last character is repeated correctly
    for repeater in repeaters:
        # remove all of the last repeating character
        repeater_head = _remove_all_last_consonants(repeater, repeater[-1])

        # check match
        if (
            (len(segment_head) >= len(repeater_head))
            and (segment_head[-len(repeater_head) :] == repeater_head)
            # matched confirmed, check it's longer
            and (len(repeater) > len(longest_word))
        ):
            longest_word = repeater
            repetition = len(repeater) - len(repeater_head)

    return longest_word, repetition
