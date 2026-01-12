# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.soundex.sound import audio_vector, word_approximation


class SoundexTestCaseX(unittest.TestCase):
    def test_word_approximation(self):
        self.assertIsNotNone(word_approximation("รถ", ["รส", "รด", "คน"]))

    def test_audio_vector(self):
        self.assertIsNotNone(audio_vector("คน"))
