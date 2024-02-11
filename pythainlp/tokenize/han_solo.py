# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-FileCopyrightText: Copyright 2019 Ponrawee Prasertsom
# SPDX-License-Identifier: Apache-2.0
"""
🪿 Han-solo: Thai syllable segmenter

GitHub: https://github.com/PyThaiNLP/Han-solo
"""
from typing import List
from pythainlp.corpus import path_pythainlp_corpus

try:
    import pycrfsuite
except ImportError:
    raise ImportError(
        "ImportError; Install pycrfsuite by pip install python-crfsuite"
    )

tagger = pycrfsuite.Tagger()
tagger.open(path_pythainlp_corpus("han_solo.crfsuite"))


class Featurizer:
    #  This class from ssg at https://github.com/ponrawee/ssg.

    def __init__(self, N=2, sequence_size=1, delimiter=None):
        self.N = N
        self.delimiter = delimiter
        self.radius = N + sequence_size

    def pad(self, sentence, padder="#"):
        return padder * (self.radius) + sentence + padder * (self.radius)

    def featurize(
        self, sentence, padding=True, indiv_char=True, return_type="list"
    ):
        if padding:
            sentence = self.pad(sentence)
        all_features = []
        all_labels = []
        skip_next = False
        for current_position in range(
            self.radius, len(sentence) - self.radius + 1
        ):
            if skip_next:
                skip_next = False
                continue
            features = {}
            if return_type == "list":
                features = []
            cut = 0
            char = sentence[current_position]
            if char == self.delimiter:
                cut = 1
                skip_next = True
            counter = 0
            chars_left = ""
            chars_right = ""
            chars = ""
            abs_index_left = current_position  # left start at -1
            abs_index_right = current_position - 1  # right start at 0
            while counter < self.radius:
                abs_index_left -= (
                    1  # สมมุติตำแหน่งที่ 0 จะได้ -1, -2, -3, -4, -5 (radius = 5)
                )
                char_left = sentence[abs_index_left]
                while char_left == self.delimiter:
                    abs_index_left -= 1
                    char_left = sentence[abs_index_left]
                relative_index_left = -counter - 1
                # เก็บตัวหนังสือ
                chars_left = char_left + chars_left
                # ใส่ลง feature
                if indiv_char:
                    left_key = "|".join([str(relative_index_left), char_left])
                    if return_type == "dict":
                        features[left_key] = 1
                    else:
                        features.append(left_key)

                abs_index_right += (
                    1  # สมมุติคือตำแหน่งที่ 0 จะได้ 0, 1, 2, 3, 4 (radius = 5)
                )
                char_right = sentence[abs_index_right]
                while char_right == self.delimiter:
                    abs_index_right += 1
                    char_right = sentence[abs_index_right]
                relative_index_right = counter
                chars_right += char_right
                if indiv_char:
                    right_key = "|".join(
                        [str(relative_index_right), char_right]
                    )
                    if return_type == "dict":
                        features[right_key] = 1
                    else:
                        features.append(right_key)

                counter += 1

            chars = chars_left + chars_right
            for i in range(0, len(chars) - self.N + 1):
                ngram = chars[i : i + self.N]
                ngram_key = "|".join([str(i - self.radius), ngram])
                if return_type == "dict":
                    features[ngram_key] = 1
                else:
                    features.append(ngram_key)
            all_features.append(features)
            if return_type == "list":
                cut = str(cut)
            all_labels.append(cut)

        return {"X": all_features, "Y": all_labels}


_to_feature = Featurizer()


def segment(text: str) -> List[str]:
    x = _to_feature.featurize(text)["X"]
    y_pred = tagger.tag(x)
    list_cut = []
    for j, k in zip(list(text), y_pred):
        if k == "1":
            list_cut.append(j)
        else:
            list_cut[-1] += j
    return list_cut
