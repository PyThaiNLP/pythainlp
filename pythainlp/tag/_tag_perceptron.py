# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Perceptron Tagger.

This tagger is a port of the Textblob Averaged Perceptron Tagger
Author: Matthew Honnibal <honnibal+gh@gmail.com>,
        Long Duong <longdt219@gmail.com> (NLTK port)
        Wannaphong Phatthiyaphaibun <wannaphong@pythainlp.org> (PyThaiNLP port)
URL: <https://github.com/sloria/textblob-aptagger>
     <https://nltk.org/>

Copyright 2013 Matthew Honnibal
NLTK modifications Copyright 2015 The NLTK Project
PyThaiNLP modifications Copyright 2020 PyThaiNLP Project

This tagger is provided under the terms of the MIT License.
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from collections.abc import Iterable


class AveragedPerceptron:
    """
    Averaged perceptron, as implemented by Matthew Honnibal.

    See more implementation details here:
    https://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/
    """

    weights: dict[str, dict[str, float]]
    classes: set[str]
    _totals: dict[tuple[str, str], float]
    _tstamps: dict[tuple[str, str], int]
    i: int

    def __init__(self) -> None:
        # Each feature gets its own weight vector,
        # so weights is a dict-of-dicts
        self.weights: dict[str, dict[str, float]] = {}
        self.classes: set[str] = set()
        # The accumulated values, for the averaging. These will be keyed by
        # feature/class tuples
        self._totals: dict[tuple[str, str], float] = defaultdict(float)
        # The last time the feature was changed, for the averaging. Also
        # keyed by feature/class tuples
        # (tstamps is short for timestamps)
        self._tstamps: dict[tuple[str, str], int] = defaultdict(int)
        # Number of instances seen
        self.i: int = 0

    def predict(self, features: dict[str, float]) -> str:
        """
        Return the best label for the features.

        The label is the one with the highest dot product of the features
        and the current weights.

        :param dict[str, float] features: feature values
        :return: best label
        :rtype: str
        """
        scores: dict[str, float] = defaultdict(float)
        for feat, value in features.items():
            if feat not in self.weights or value == 0:
                continue
            weights = self.weights[feat]
            for label, weight in weights.items():
                scores[label] += value * weight
        # Do a secondary alphabetic sort, for stability
        return max(self.classes, key=lambda label: (scores[label], label))

    def update(
        self, truth: str, guess: str, features: dict[str, float]
    ) -> None:
        """
        Update the feature weights.

        :param str truth: correct label
        :param str guess: predicted label
        :param dict[str, float] features: feature values
        """

        def upd_feat(c: str, f: str, w: float, v: float) -> None:
            param = (f, c)
            self._totals[param] += (self.i - self._tstamps[param]) * w
            self._tstamps[param] = self.i
            self.weights[f][c] = w + v

        self.i += 1
        if truth == guess:
            return
        for f in features:
            weights = self.weights.setdefault(f, {})
            upd_feat(truth, f, weights.get(truth, 0.0), 1.0)
            upd_feat(guess, f, weights.get(guess, 0.0), -1.0)

    def average_weights(self) -> None:
        """Average the weights over all iterations."""
        for feat, weights in self.weights.items():
            new_feat_weights = {}
            for clas, weight in weights.items():
                param = (feat, clas)
                total = self._totals[param]
                total += (self.i - self._tstamps[param]) * weight
                averaged = round(total / float(self.i), 3)
                if averaged:
                    new_feat_weights[clas] = averaged
            self.weights[feat] = new_feat_weights


class PerceptronTagger:
    """
    Greedy averaged perceptron tagger, as implemented by Matthew Honnibal.

    See more implementation details here:
    https://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/

    >>> from pythainlp.tag import PerceptronTagger
    >>> tagger = PerceptronTagger()
    >>> data = [
    ...     [("คน", "N"), ("เดิน", "V")],
    ...     [("แมว", "N"), ("เดิน", "V")],
    ...     [("คน", "N"), ("วิ่ง", "V")],
    ...     [("ปลา", "N"), ("ว่าย", "V")],
    ...     [("นก", "N"), ("บิน", "V")],
    ... ]
    >>> tagger.train(data)
    >>> tagger.tag(["นก", "เดิน"])
    [('นก', 'N'), ('เดิน', 'V')]
    """

    START: list[str] = ["-START-", "-START2-"]
    END: list[str] = ["-END-", "-END2-"]
    AP_MODEL_LOC: str = ""

    model: AveragedPerceptron
    tagdict: dict[str, str]
    classes: set[str]

    def __init__(self, path: str = "") -> None:
        """
        Initialize the tagger.

        :param str path: path to the model file
        """
        self.model: AveragedPerceptron = AveragedPerceptron()
        self.tagdict: dict[str, str] = {}
        self.classes: set[str] = set()
        if path != "":
            self.AP_MODEL_LOC: str = path
            self.load(self.AP_MODEL_LOC)

    def tag(self, tokens: Iterable[str]) -> list[tuple[str, str]]:
        """
        Tag words with part-of-speech (POS) tags.

        :param Iterable[str] tokens: words to be tagged
        :return: list of tuples (word, POS tag)
        :rtype: list[tuple[str, str]]
        """
        prev, prev2 = self.START
        output = []

        context = self.START + [self._normalize(w) for w in tokens] + self.END
        for i, word in enumerate(tokens):
            tag = self.tagdict.get(word)
            if not tag:
                features = self._get_features(i, word, context, prev, prev2)
                tag = self.model.predict(features)
            output.append((word, tag))
            prev2 = prev
            prev = tag
        return output

    def train(
        self,
        sentences: Iterable[Iterable[tuple[str, str]]],
        save_loc: Optional[str] = None,
        nr_iter: int = 5,
    ) -> None:
        """
        Train a model from sentences and optionally save it.

        :param Iterable[Iterable[tuple[str, str]]] sentences: sentences of
            (word, tag) tuples
        :param Optional[str] save_loc: path to save the model as a JSON
            file; do not save if ``None``
        :param int nr_iter: number of perceptron training iterations
        """
        import random

        self._make_tagdict(sentences)
        self.model.classes = self.classes
        for _ in range(nr_iter):
            c = 0
            n = 0
            sentences_list = list(sentences)
            for sentence in sentences_list:
                words, tags = zip(*sentence)

                prev, prev2 = self.START
                context = (
                    self.START + [self._normalize(w) for w in words] + self.END
                )
                for i, word in enumerate(words):
                    guess = self.tagdict.get(word)
                    if not guess:
                        feats = self._get_features(
                            i, word, context, prev, prev2
                        )
                        guess = self.model.predict(feats)
                        self.model.update(tags[i], guess, feats)
                    prev2 = prev
                    prev = guess
                    c += guess == tags[i]
                    n += 1
            random.shuffle(sentences_list)
        self.model.average_weights()

        # save the model as JSON
        if save_loc is not None:
            data: dict[str, Any] = {}
            data["weights"] = self.model.weights
            data["tagdict"] = self.tagdict
            data["classes"] = list(self.classes)
            with open(save_loc, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

    def load(self, loc: str) -> None:
        """
        Load a saved model from a JSON file.

        :param str loc: path to the model file
        :raises OSError: if the model file cannot be opened
        """
        try:
            with open(loc, encoding="utf-8-sig") as f:
                w_td_c = json.load(f)
        except OSError as ex:
            msg = "Missing trontagger.json file."
            raise OSError(msg) from ex
        self.model.weights = w_td_c["weights"]
        self.tagdict: dict[str, list[str]] = w_td_c["tagdict"]
        self.classes: list[str] = w_td_c["classes"]
        self.model.classes = set(self.classes)

    def _normalize(self, word: str) -> str:
        """
        Normalize a word in preprocessing.

        - All words are lowercased
        - Four-digit numbers are represented as !YEAR
        - Other numbers starting with a digit are represented as !DIGITS
        - Words with a hyphen, except at the start, are represented as
          !HYPHEN

        :param str word: word to be normalized
        :return: normalized word
        :rtype: str
        """
        if "-" in word and word[0] != "-":
            return "!HYPHEN"
        if word.isdigit() and len(word) == 4:
            return "!YEAR"
        if word[0].isdigit():
            return "!DIGITS"
        return word.lower()

    def _get_features(
        self, i: int, word: str, context: list[str], prev: str, prev2: str
    ) -> dict[str, float]:
        """
        Map a word and its context to a feature representation.

        The representation is a dict of feature name to value. If the
        features change, train a new model.

        :param int i: index of the word
        :param str word: word to extract features from
        :param list[str] context: normalized words with start and end markers
        :param str prev: tag of the previous word
        :param str prev2: tag of the word before the previous word
        :return: feature values
        :rtype: dict[str, float]
        """

        def add(name: str, *args: str) -> None:
            features[" ".join((name,) + tuple(args))] += 1

        i += len(self.START)
        features: dict[str, float] = defaultdict(int)
        # It's useful to have a constant feature,
        # which acts sort of like a prior
        add("bias")
        add("i suffix", word[-3:])
        add("i pref1", word[0])
        add("i-1 tag", prev)
        add("i-2 tag", prev2)
        add("i tag+i-2 tag", prev, prev2)
        add("i word", context[i])
        add("i-1 tag+i word", prev, context[i])
        add("i-1 word", context[i - 1])
        add("i-1 suffix", context[i - 1][-3:])
        add("i-2 word", context[i - 2])
        add("i+1 word", context[i + 1])
        add("i+1 suffix", context[i + 1][-3:])
        add("i+2 word", context[i + 2])
        return features

    def _make_tagdict(
        self, sentences: Iterable[Iterable[tuple[str, str]]]
    ) -> None:
        """Make a tag dictionary for words with a single dominant tag."""
        counts: dict[str, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        for sentence in sentences:
            for word, tag in sentence:
                counts[word][tag] += 1
                self.classes.add(tag)
        freq_thresh = 20
        ambiguity_thresh = 0.97
        for word, tag_freqs in counts.items():
            tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
            n = sum(tag_freqs.values())
            # Don't add rare words to the tag dictionary
            # Only add quite unambiguous words
            if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
                self.tagdict[word] = tag
