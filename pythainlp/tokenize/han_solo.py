# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileCopyrightText: Copyright 2019 Ponrawee Prasertsom
# SPDX-License-Identifier: Apache-2.0
"""🪿 Han-solo: Thai syllable segmenter

GitHub: https://github.com/PyThaiNLP/Han-solo
"""

from __future__ import annotations

import threading
from importlib.resources import as_file, files
from typing import Any, Optional

try:
    import pycrfsuite
except ImportError as ex:
    raise ImportError(
        "ImportError; Install pycrfsuite by pip install python-crfsuite"
    ) from ex

_tagger: Optional[pycrfsuite.Tagger] = None
_model_file_ctx: Optional[Any] = (
    None  # File context manager kept alive for program lifetime
)
_load_lock: threading.Lock = threading.Lock()  # Thread safety for lazy loading


def _get_tagger() -> pycrfsuite.Tagger:
    """Load the tagger model once, in a thread-safe way.

    The file context manager stays open for the life of the program,
    so a temporary model file is not removed while the tagger uses it.
    """
    global _tagger, _model_file_ctx
    if _tagger is None:
        with _load_lock:
            # Check again: another thread may have loaded it
            if _tagger is None:
                _tagger = pycrfsuite.Tagger()
                corpus_files = files("pythainlp.corpus")
                model_file = corpus_files.joinpath("han_solo.crfsuite")
                _model_file_ctx = as_file(model_file)
                model_path = _model_file_ctx.__enter__()
                _tagger.open(str(model_path))
    return _tagger


class Featurizer:
    #  This class from ssg at https://github.com/ponrawee/ssg.

    N: int
    delimiter: Optional[str]
    radius: int

    def __init__(
        self,
        N: int = 2,
        sequence_size: int = 1,
        delimiter: Optional[str] = None,
    ) -> None:
        self.N: int = N
        self.delimiter: Optional[str] = delimiter
        self.radius: int = N + sequence_size

    def pad(self, sentence: str, padder: str = "#") -> str:
        return padder * (self.radius) + sentence + padder * (self.radius)

    def _skip_delimiter(
        self, sentence: str, abs_index: int, step: int
    ) -> tuple[int, str]:
        """Skip the delimiter, moving ``abs_index`` by ``step``.

        :return: the new index and the character at that index
        """
        char = sentence[abs_index]
        while char == self.delimiter:
            abs_index += step
            char = sentence[abs_index]
        return abs_index, char

    def _context_features(
        self, sentence: str, current_position: int, indiv_char: bool
    ) -> list[str]:
        """Extract features around ``current_position``."""
        features: list[str] = []
        chars_left = ""
        chars_right = ""
        abs_index_left = current_position  # left start at -1
        abs_index_right = current_position - 1  # right start at 0
        for counter in range(self.radius):
            abs_index_left -= (
                1  # สมมุติตำแหน่งที่ 0 จะได้ -1, -2, -3, -4, -5 (radius = 5)
            )
            abs_index_left, char_left = self._skip_delimiter(
                sentence, abs_index_left, -1
            )
            # เก็บตัวหนังสือ
            chars_left = char_left + chars_left
            # ใส่ลง feature
            if indiv_char:
                features.append("|".join([str(-counter - 1), char_left]))

            abs_index_right += (
                1  # สมมุติคือตำแหน่งที่ 0 จะได้ 0, 1, 2, 3, 4 (radius = 5)
            )
            abs_index_right, char_right = self._skip_delimiter(
                sentence, abs_index_right, 1
            )
            chars_right += char_right
            if indiv_char:
                features.append("|".join([str(counter), char_right]))

        chars = chars_left + chars_right
        for i in range(len(chars) - self.N + 1):
            ngram = chars[i : i + self.N]
            features.append("|".join([str(i - self.radius), ngram]))
        return features

    def featurize(
        self,
        sentence: str,
        padding: bool = True,
        indiv_char: bool = True,
        return_type: str = "list",
    ) -> dict[str, list[Any]]:
        if padding:
            sentence = self.pad(sentence)
        all_features_list: list[list[str]] = []
        all_labels_int: list[int] = []
        skip_next = False
        for current_position in range(
            self.radius, len(sentence) - self.radius + 1
        ):
            if skip_next:
                skip_next = False
                continue
            cut = 0
            if sentence[current_position] == self.delimiter:
                cut = 1
                skip_next = True
            all_features_list.append(
                self._context_features(sentence, current_position, indiv_char)
            )
            all_labels_int.append(cut)

        if return_type == "list":
            return {
                "X": all_features_list,
                "Y": [str(label) for label in all_labels_int],
            }
        return {
            "X": [
                dict.fromkeys(feature_list, 1)
                for feature_list in all_features_list
            ],
            "Y": all_labels_int,
        }


_to_feature: Featurizer = Featurizer()


def segment(text: str) -> list[str]:
    tagger = _get_tagger()
    x = _to_feature.featurize(text)["X"]
    y_pred = tagger.tag(x)
    list_cut: list[str] = []
    for j, k in zip(list(text), y_pred):
        if k == "1" or not list_cut:
            list_cut.append(j)
        else:
            list_cut[-1] += j
    return list_cut
