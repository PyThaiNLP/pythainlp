# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import re
import sys
from typing import List, Tuple

import numpy as np
import pandas as pd

SEPARATOR = "|"

# regex for removing one space surrounded by separators, i.e. | |
SURROUNDING_SEPS_RX = re.compile(
    "{sep}? ?{sep}$".format(sep=re.escape(SEPARATOR))
)

# regex for removing repeated separators, i.e. ||||
MULTIPLE_SEPS_RX = re.compile("{sep}+".format(sep=re.escape(SEPARATOR)))

# regex for removing tags, i.e. <NE>, </NE>
TAG_RX = re.compile(r"<\/?[A-Z]+>")

# regex for removing trailing separators, i.e.  a|dog| -> a|dog
TAILING_SEP_RX = re.compile("{sep}$".format(sep=re.escape(SEPARATOR)))


def _f1(precision: float, recall: float) -> float:
    """
    Compute f1.

    :param float precision
    :param float recall

    :return: f1
    :rtype: float
    """
    if precision == recall == 0:
        return 0
    return 2 * precision * recall / (precision + recall)


def _flatten_result(my_dict: dict, sep: str = ":") -> dict:
    """
    Flatten two-dimension dictionary.

    Use keys in the first dimension as a prefix for keys in the second dimension.
    For example,
    my_dict = { "a": { "b": 7 } }
    flatten(my_dict)
    { "a:b": 7 }


    :param dict my_dict: dictionary containing stats
    :param str sep: separator between the two keys (default: ":")

    :return: a one-dimension dictionary with keys combined
    :rtype: dict[str, float | str]
    """
    items = []
    for k1, kv2 in my_dict.items():
        for k2, v in kv2.items():
            new_key = f"{k1}{sep}{k2}"
            items.append((new_key, v))

    return dict(items)


def benchmark(ref_samples: List[str], samples: List[str]) -> pd.DataFrame:
    """
    Performance benchmarking for samples.

    Please see :meth:`pythainlp.benchmarks.word_tokenization.compute_stats` for
    the computed metrics.

    :param list[str] ref_samples: ground truth for samples
    :param list[str] samples: samples that we want to evaluate

    :return: dataframe with row x col = len(samples) x len(metrics)
    :rtype: pandas.DataFrame
    """
    results = []
    for i, (r, s) in enumerate(zip(ref_samples, samples)):
        try:
            r, s = preprocessing(r), preprocessing(s)
            if r and s:
                stats = compute_stats(r, s)
                stats = _flatten_result(stats)
                stats["expected"] = r
                stats["actual"] = s
                results.append(stats)
        except:
            reason = """
[Error]
Reason: %s

Pair (i=%d)
--- label
%s
--- sample
%s
""" % (
                sys.exc_info(),
                i,
                r,
                s,
            )
            raise SystemExit(reason)

    return pd.DataFrame(results)


def preprocessing(txt: str, remove_space: bool = True) -> str:
    """
    Clean up text before performing evaluation.

    :param str text: text to be preprocessed
    :param bool remove_space: whether to remove white space

    :return: preprocessed text
    :rtype: str
    """
    txt = re.sub(SURROUNDING_SEPS_RX, "", txt)

    if remove_space:
        txt = re.sub(r"\s+", "", txt)

    txt = re.sub(MULTIPLE_SEPS_RX, SEPARATOR, txt)

    txt = re.sub(TAG_RX, "", txt)

    txt = re.sub(TAILING_SEP_RX, "", txt).strip()

    return txt


def compute_stats(ref_sample: str, raw_sample: str) -> dict:
    """
    Compute statistics for tokenization quality

    These statistics include:

    **Character-Level**:
      True Positive, False Positive, True Negative, False Negative, Precision, Recall, and f1
    **Word-Level**:
      Precision, Recall, and f1
    **Other**:
      - Correct tokenization indicator: {0, 1} sequence indicating that the corresponding
        word is tokenized correctly.

    :param str ref_sample: ground truth for samples
    :param str samples: samples that we want to evaluate

    :return: metrics at character- and word-level and indicators of correctly tokenized words
    :rtype: dict[str, float | str]
    """
    ref_sample = _binary_representation(ref_sample)
    sample = _binary_representation(raw_sample)

    # Compute character-level statistics
    c_pos_pred, c_neg_pred = np.argwhere(sample == 1), np.argwhere(sample == 0)

    c_pos_pred = c_pos_pred[c_pos_pred < ref_sample.shape[0]]
    c_neg_pred = c_neg_pred[c_neg_pred < ref_sample.shape[0]]

    c_tp = np.sum(ref_sample[c_pos_pred] == 1)
    c_fp = np.sum(ref_sample[c_pos_pred] == 0)

    c_tn = np.sum(ref_sample[c_neg_pred] == 0)
    c_fn = np.sum(ref_sample[c_neg_pred] == 1)

    # Compute word-level statistics

    # Find correctly tokenized words in the reference sample
    word_boundaries = _find_word_boundaries(ref_sample)

    # Find correctly tokenized words in the sample
    ss_boundaries = _find_word_boundaries(sample)
    tokenization_indicators = _find_words_correctly_tokenised(
        word_boundaries, ss_boundaries
    )

    correctly_tokenised_words = np.sum(tokenization_indicators)

    tokenization_indicators = list(
        map(str, tokenization_indicators)
    )

    return {
        "char_level": {
            "tp": c_tp,
            "fp": c_fp,
            "tn": c_tn,
            "fn": c_fn,
        },
        "word_level": {
            "correctly_tokenised_words": correctly_tokenised_words,
            "total_words_in_sample": np.sum(sample),
            "total_words_in_ref_sample": np.sum(ref_sample),
        },
        "global": {
            "tokenisation_indicators": "".join(tokenization_indicators)
        },
    }


def _binary_representation(txt: str, verbose: bool = False):
    """
    Transform text into {0, 1} sequence.

    where (1) indicates that the corresponding character is the beginning of
    a word. For example, ผม|ไม่|ชอบ|กิน|ผัก -> 10100...

    :param str txt: input text that we want to transform
    :param bool verbose: for debugging purposes

    :return: {0, 1} sequence
    :rtype: str
    """
    chars = np.array(list(txt))

    boundary = np.argwhere(chars == SEPARATOR).reshape(-1)
    boundary = boundary - np.array(range(boundary.shape[0]))

    bin_rept = np.zeros(len(txt) - boundary.shape[0])
    bin_rept[list(boundary) + [0]] = 1

    sample_wo_seps = list(txt.replace(SEPARATOR, ""))

    # sanity check
    assert len(sample_wo_seps) == len(bin_rept)

    if verbose:
        for c, m in zip(sample_wo_seps, bin_rept):
            print("%s -- %d" % (c, m))

    return bin_rept


def _find_word_boundaries(bin_reps) -> list:
    """
    Find the starting and ending location of each word.

    :param str bin_reps: binary representation of a text

    :return: list of tuples (start, end)
    :rtype: list[tuple(int, int)]
    """
    boundary = np.argwhere(bin_reps == 1).reshape(-1)
    start_idx = boundary
    end_idx = boundary[1:].tolist() + [bin_reps.shape[0]]

    return list(zip(start_idx, end_idx))


def _find_words_correctly_tokenised(
    ref_boundaries: List[Tuple[int, int]],
    predicted_boundaries: List[Tuple[int, int]],
) -> Tuple[int]:
    """
    Find whether each word is correctly tokenized.

    :param list[tuple(int, int)] ref_boundaries: word boundaries of reference tokenization
    :param list[tuple(int, int)] predicted_boundaries: word boundareies of predicted tokenization

    :return: binary sequence where 1 indicates the corresponding word is tokenized correctly
    :rtype: tuple[int]
    """
    ref_b = dict(zip(ref_boundaries, [1] * len(ref_boundaries)))

    labels = tuple(map(lambda x: ref_b.get(x, 0), predicted_boundaries))
    return labels
