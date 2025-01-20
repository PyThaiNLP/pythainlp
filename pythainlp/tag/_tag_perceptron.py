# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
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
import json
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple, Union


class AveragedPerceptron():
    """
    An averaged perceptron, as implemented by Matthew Honnibal.

    See more implementation details here:
        http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/
    """

    def __init__(self) -> None:
        # Each feature gets its own weight vector,
        # so weights is a dict-of-dicts
        self.weights = {}
        self.classes = set()
        # The accumulated values, for the averaging. These will be keyed by
        # feature/class tuples
        self._totals = defaultdict(int)
        # The last time the feature was changed, for the averaging. Also
        # keyed by feature/class tuples
        # (tstamps is short for timestamps)
        self._tstamps = defaultdict(int)
        # Number of instances seen
        self.i = 0

    def predict(self, features: Dict):
        """
        Dot-product the features and current weights and return the best
        label.
        """
        scores = defaultdict(float)
        for feat, value in features.items():
            if feat not in self.weights or value == 0:
                continue
            weights = self.weights[feat]
            for label, weight in weights.items():
                scores[label] += value * weight
        # Do a secondary alphabetic sort, for stability
        return max(self.classes, key=lambda label: (scores[label], label))

    def update(self, truth, guess, features: Dict) -> None:
        """Update the feature weights."""

        def upd_feat(c, f, w, v):
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
        """Average weights from all iterations."""
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
    Greedy Averaged Perceptron tagger, as implemented by Matthew Honnibal.

    See more implementation details here:
        http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/

    >>> from pythainlp.tag import PerceptronTagger
    >>> tagger = PerceptronTagger()
    >>> data = [
            [("คน", "N"), ("เดิน", "V")],
            [("แมว", "N"), ("เดิน", "V")],
            [("คน", "N"), ("วิ่ง", "V")],
            [("ปลา", "N"), ("ว่าย", "V")],
            [("นก", "N"), ("บิน", "V")],
        ]
    >>> tagger.train(data)
    >>> tagger.tag(["นก", "เดิน])
    [('นก', 'N'), ('เดิน', 'V')]

    """

    START = ["-START-", "-START2-"]
    END = ["-END-", "-END2-"]
    AP_MODEL_LOC = ""

    def __init__(self, path: str = "") -> None:
        """
        :param str path: model path
        """
        self.model = AveragedPerceptron()
        self.tagdict = {}
        self.classes = set()
        if path != "":
            self.AP_MODEL_LOC = path
            self.load(self.AP_MODEL_LOC)

    def tag(self, tokens: Iterable[str]) -> List[Tuple[str, str]]:
        """Tags a string `tokens`."""
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
        sentences: Iterable[Iterable[Tuple[str, str]]],
        save_loc: Union[str, None] = None,
        nr_iter: int = 5,
    ) -> None:
        """
        Train a model from sentences, and save it at ``save_loc``.
        ``nr_iter`` controls the number of Perceptron training iterations.

        :param sentences: A list of (words, tags) tuples.
        :param save_loc: If not ``None``, saves a pickled model in this \
            location.
        :param nr_iter: Number of training iterations.
        """
        import random

        self._make_tagdict(sentences)
        self.model.classes = self.classes
        for _ in range(nr_iter):
            c = 0
            n = 0
            for sentence in sentences:
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
            random.shuffle(sentences)
        self.model.average_weights()

        # save the model
        if save_loc is not None:
            data = {}
            data["weights"] = self.model.weights
            data["tagdict"] = self.tagdict
            data["classes"] = list(self.classes)
            with open(save_loc, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

    def load(self, loc: str) -> None:
        """
        Load a pickled model.
        :param str loc: model path
        """
        try:
            with open(loc, "r", encoding="utf-8-sig") as f:
                w_td_c = json.load(f)
        except IOError:
            msg = "Missing trontagger.json file."
            raise IOError(msg)
        self.model.weights = w_td_c["weights"]
        self.tagdict = w_td_c["tagdict"]
        self.classes = w_td_c["classes"]
        self.model.classes = set(self.classes)

    def _normalize(self, word: str) -> str:
        """
        Normalization used in pre-processing.

        - All words are lower cased
        - Digits in the range 1800-2100 are represented as !YEAR;
        - Other digits are represented as !DIGITS

        :rtype: str
        """
        if "-" in word and word[0] != "-":
            return "!HYPHEN"
        elif word.isdigit() and len(word) == 4:
            return "!YEAR"
        elif word[0].isdigit():
            return "!DIGITS"
        else:
            return word.lower()

    def _get_features(
        self, i: int, word: str, context: List[str], prev: str, prev2: str
    ) -> Dict:
        """
        Map tokens into a feature representation, implemented as a
        {hashable: float} dict. If the features change, a new model must be
        trained.
        """

        def add(name: str, *args):
            features[" ".join((name,) + tuple(args))] += 1

        i += len(self.START)
        features = defaultdict(int)
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
        self, sentences: Iterable[Iterable[Tuple[str, str]]]
    ) -> None:
        """Make a tag dictionary for single-tag words."""
        counts = defaultdict(lambda: defaultdict(int))
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
