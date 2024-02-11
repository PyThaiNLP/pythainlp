# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Removement of repeated consonants at the end of words
"""
from pythainlp.corpus import thai_words
from pythainlp.util.trie import Trie
from pythainlp import thai_consonants as consonants
from typing import Iterable, List, Tuple

# used by remove_trailing_repeat_consonants()
# contains all words that has repeating consonants at the end
# for each consonant
# when dictionary updated, this should be updated too
# key: consonant
# value: list of words that has repeating consonants at the end
last_consonants_repeaters = {}


def remove_trailing_repeat_consonants(
    text: str,
    custom_dict: Iterable[str] = [],
    has_dictionary_updated: bool = True,
) -> str:
    """
    Remove repeating consonants at the last of the sentence.

    This function will remove the repeating consonants
    before a whitespace, new line or at the last
    so that the last word matches a word in the given dictionary.
    If there is no match, the repeating consonants will be
    reduced to one.
    If there are several match, the longest word will be used.
    Since this function uses a dictionary, the result may differs
    depending on the dictionary used.
    Plus, it is recommended to use normalize() to have a better result.

    :param str text: input text
    :param Trie dictionary: Trie dictionary to check the last word.
    If None, pythainlp.corpus.thai_words() will be used
    :param bool has_dictionary_updated: If the dictionary is updated 
    or the first time using in the kernel, set this true.
    If not, set this false to save time.
    :return: text without repeating Thai consonants
    :rtype: str

    :Example:
    ::

        from pythainlp.util import remove_trailing_repeat_consonants
        from pythainlp.util import dict_trie

        # use default dictionary (pythainlp.corpus.thai_words())
        remove_trailing_repeat_consonants('เริ่ดดดดดดดด')
        # output: เริ่ด

        remove_trailing_repeat_consonants('อืมมมมมมมมมมมมมมม')
        # output: อืมมม
        # "อืมมม" is in the default dictionary

        # use custom dictionary
        custom_dict = dict_trie(["อืมมมมม"])
        remove_trailing_repeat_consonants('อืมมมมมมมมมมมมมมม', custom_dict)
        # output: อืมมมมม

        # long text
        remove_trailing_repeat_consonants('อืมมมมมมมมมมมมม คุณมีบุคลิกที่เริ่ดดดดด '\
        'ฉันจะให้เกรดดีกับคุณณณ\nนี่เป็นความลับบบบบ')
        # output: อืมมม คุณมีบุคลิกที่เริ่ด ฉันจะให้เกรดดีกับคุณ
        #         นี่เป็นความลับ
    """
    # use default dictionary if not given
    if not custom_dict:
        custom_dict = thai_words()

    # update repeaters dictionary if not updated
    if has_dictionary_updated:
        _update_consonant_repeaters(custom_dict)

    # seperate by newline
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
    Remove repeating consonants at the last of the segment.

    This function process only at the last of the given text.
    Details is same as remove_repeat_consonants().

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
        # has repiitition
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

        # make the repition to once
        segment = segment_head + (dup * 1)

    return segment


def _remove_all_last_consonants(text: str, dup: str) -> str:
    """
    Reduce repeating characters at the end of the text.

    This function will remove the repeating characters at the last.
    The text just before the repeating characters will be returned.

    :param str text: input text
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
    Update dictionary of all words that has
    repeating consonants at the end from the dictionary.

    Search all words in the dictionary that has more than 1 consonants
    repeating at the end and store them in the global dictionary.

    :param str consonant: consonant to be searched
    :param Trie dictionary: Trie dictionary to search
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

    This function checks if the word has
    more than 1 repeating consonants at the end.

    :param str word: word to be checked
    :return: True if the word has repeating consonants at the end.
    :rtype: bool
    """
    return (
        (len(word) > 1) and (word[-1] == word[-2]) and (word[-1] in consonants)
    )


def _find_longest_consonant_repeaters_match(
    segment_head: str, repeaters: List[str]
) -> Tuple[str, int]:
    """
    Find the longest word that matches the segment.

    Find the longest word that matches the last
    of the segment from the given repeaters list.
    This returns the word and
    how much the last character is repeated correctly.

    :param str segment: segment of text
    :param List[str] repeaters: list of words
    that has repeating consonants at the end
    :return: "tuple of the word" and
    "how much the last character is repeated correctly"
    If none, ("", 0) will be returned.
    :rtype: Tuple[str, int]
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
