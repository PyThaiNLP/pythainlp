# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for expand_maiyamok and longest_common_subsequence.

Golden data was recorded from the pre-refactor implementation.
"""

import unittest

from pythainlp.util import expand_maiyamok
from pythainlp.util.lcs import longest_common_subsequence

# (token list, expected tokens)
_MAIYAMOK_LISTS = [
    (["คน", "ๆ", "นก"], ["คน", "คน", "นก"]),
    (["คนๆ", "นก"], ["คน", "คน", "นก"]),
    (["นกๆๆ"], ["นก", "นก", "นก"]),
    (["นกๆ ๆ"], ["นก", "นก", "นก"]),
    (["นกๆคน"], ["นก", "นก", "คน"]),
    (["ๆ"], []),
    (["ๆ", "ๆ"], []),
    ([], []),
    ([""], []),
    (["คน", " ", "ๆ"], ["คน", "คน"]),
    (["คน", "  ", "ๆ", "นก"], ["คน", "คน", "นก"]),
    (["ๆ", "คน"], ["คน"]),
    ([" ", "ๆ", "คน"], ["คน"]),
    (["คน", "ๆ", " ", "นก"], ["คน", "คน", " ", "นก"]),
    (["a", "b", "ๆ", "ๆ", "c"], ["a", "b", "b", "b", "c"]),
]

# (text, expected tokens); the text is tokenized first.
_MAIYAMOK_TEXTS = [
    ("คนๆนก", ["คน", "คน", "นก"]),
    ("", []),
    ("นกๆๆ", ["นก", "นก", "นก"]),
    ("นกๆ ๆ", ["นก", "นก", "นก"]),
    ("สวัสดีๆ ครับ", ["สวัสดี", "สวัสดี", " ", "ครับ"]),
    ("คนไทยๆ", ["คนไทย", "คนไทย"]),
    (" ๆ", []),
]

# (str1, str2, expected subsequence)
_LCS = [
    ("ABCBDAB", "BDCAB", "BDAB"),
    ("", "abc", ""),
    ("abc", "", ""),
    ("", "", ""),
    ("abc", "abc", "abc"),
    ("abc", "def", ""),
    ("AGGTAB", "GXTXAYB", "GTAB"),
    ("ทดสอบ", "ทดลอง", "ทดอ"),
    ("กกกกก", "กกก", "กกก"),
    ("abcdef", "fbdamn", "bd"),
    ("aab", "azb", "ab"),
    ("xyz", "zyx", "z"),
    ("cc", "aa", ""),
    ("abccaa", "aaa", "aaa"),
    ("babbca", "acb", "ac"),
    ("bbcacbc", "accca", "acc"),
    ("babb", "acbacbb", "babb"),
    ("c", "bc", "c"),
    ("cabc", "caccaccc", "cac"),
    ("cac", "aaa", "a"),
    ("cbcbbab", "babc", "bab"),
    ("ac", "ccacbacb", "ac"),
    ("aaabcbacb", "ac", "ac"),
    ("ababacab", "cccaaa", "aaa"),
    ("baacba", "babcabacb", "bacba"),
    ("bb", "abbbcccbb", "bb"),
    ("bcbbaca", "bccbbaba", "bcbbaa"),
    ("ccbc", "cbbcaa", "cbc"),
    ("b", "cba", "b"),
    ("cacacbc", "aaccbc", "aacbc"),
    ("caaccb", "aaacaaccb", "caaccb"),
    ("", "acba", ""),
    ("aabbc", "abccaa", "abc"),
    ("abbb", "babaa", "bb"),
    ("caab", "baacc", "aa"),
    ("accaaaca", "cbbb", "c"),
]


class ExpandMaiyamokTestCase(unittest.TestCase):
    def test_token_lists(self) -> None:
        for tokens, expected in _MAIYAMOK_LISTS:
            with self.subTest(tokens=tokens):
                self.assertEqual(expand_maiyamok(tokens), expected)

    def test_texts(self) -> None:
        for text, expected in _MAIYAMOK_TEXTS:
            with self.subTest(text=text):
                self.assertEqual(expand_maiyamok(text), expected)

    def test_does_not_modify_input(self) -> None:
        tokens = ["คน", "ๆ", "นก"]
        expand_maiyamok(tokens)
        self.assertEqual(tokens, ["คน", "ๆ", "นก"])

    def test_invalid_input(self) -> None:
        for value in (None, 5):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    expand_maiyamok(value)  # type: ignore[arg-type]
        ints = [1, 2]
        with self.assertRaises(TypeError):
            expand_maiyamok(ints)  # type: ignore[arg-type]


class LongestCommonSubsequenceTestCase(unittest.TestCase):
    def test_golden(self) -> None:
        for str1, str2, expected in _LCS:
            with self.subTest(str1=str1, str2=str2):
                self.assertEqual(
                    longest_common_subsequence(str1, str2), expected
                )

    def test_sequences(self) -> None:
        self.assertEqual(
            longest_common_subsequence(["a", "b", "c"], ["b", "c"]),  # type: ignore[arg-type]
            "bc",
        )
        self.assertEqual(
            longest_common_subsequence(("a", "b"), ("a",)),  # type: ignore[arg-type]
            "a",
        )

    def test_invalid_input(self) -> None:
        for args in ((None, "a"), ("a", None), (1, "a"), ("a", 5)):
            with self.subTest(args=args):
                with self.assertRaises(TypeError):
                    longest_common_subsequence(*args)

    def test_long_input(self) -> None:
        text = "ก" * 300 + "ข" * 300
        self.assertEqual(longest_common_subsequence(text, text), text)


if __name__ == "__main__":
    unittest.main()
