# -*- coding: utf-8 -*-

import re
import sys

import numpy as np
import pandas as pd


SEPARATOR = "|"

# regex for removing to a space surrounded by separators, i.e. | |
SURROUNDING_SEPS_RX = re.compile(
    "{sep}? ?{sep}$".format(sep=re.escape(SEPARATOR))
)

# regex for removing repeated separators, i.e. ||||
MULTIPLE_SEPS_RX = re.compile("{sep}+".format(sep=re.escape(SEPARATOR)))

# regex for removing tags, i.e. <NE>, </NE> 
TAG_RX = re.compile("<\/?[A-Z]+>")

# regex for tailing separator, i.e.  a|dog| -> a|dog
TAILING_SEP_RX = re.compile("{sep}$".format(sep=re.escape(SEPARATOR)))


def _f1(precision: float, recall: float) -> float:
    """
    Compute f1

    :param float precision
    :param float recall

    :return: f1
    :rtype: float
    """
    if precision == recall == 0:
        return 0
    return 2*precision*recall / (precision + recall)


def _flatten_result(my_dict: dict, sep: str = ":") -> dict:
    """
    Flatten two-level dictionary

    Use keys in the first level as a prefix for keys in the two levels.
    For example,
    my_dict = { "a": { "b": 7 } } 
    flatten(my_dict)
    { "a:b": 7 }


    :param dict my_dict: contains stats dictionary
    :param str sep: separator between the two keys (default: ":")

    :return: a one-level dictionary with key combined
    :rtype: dict[str, float | str]
    """
    items = []
    for k1, kv2 in my_dict.items():
        for k2, v in kv2.items():
            new_key = f"{k1}{sep}{k2}"
            items.append((new_key, v))

    return dict(items)


def benchmark(ref_samples: list, samples: list):
    """
    Performace benchmark of samples

    Please see :meth:`pythainlp.benchmarks.word_tokenization.compute_stats` for
    metrics being computed.

    :param list[str] ref_samples: ground truth samples
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
""" % (sys.exc_info(), i, r, s)

            raise SystemExit(reason)

    return pd.DataFrame(results)


def preprocessing(txt: str, remove_space: bool = True) -> str:
    """
    Clean up text before performing evaluation

    :param str text: text to be preprocessed
    :param bool remove_space: whether remove white space

    :return: preprocessed text
    :rtype: str
    """
    txt = re.sub(SURROUNDING_SEPS_RX, "", txt)

    if remove_space:
        txt = re.sub("\s+", "", txt)

    txt = re.sub(
        MULTIPLE_SEPS_RX,
        SEPARATOR,
        txt
    )

    txt = re.sub(TAG_RX, "", txt)

    txt = re.sub(TAILING_SEP_RX, "", txt).strip()

    return txt


def compute_stats(ref_sample: str, raw_sample: str) -> dict:
    """
    Compute statistics for tokenization quality

    These statistics includes:

    **Character-Level**:
      True Positive, False Positive, True Negative, False Negative, Precision, Recall, and f1
    **Word-Level**:
      Precision, Recall, and f1
    **Other**:
      - Correct tokenization indicator: {0, 1} sequence indicating the correspoding
        word is tokenized correctly.

    :param str ref_sample: ground truth samples
    :param str samples samples that we want to evaluate

    :return: metrics in character and word-level and correctly tokenized word indicators
    :rtype: dict[str, float | str]
    """
    ref_sample = _binary_representation(ref_sample)
    sample = _binary_representation(raw_sample)

    # Compute charater-level statistics
    c_pos_pred, c_neg_pred = np.argwhere(sample == 1), np.argwhere(sample == 0)

    c_pos_pred = c_pos_pred[c_pos_pred < ref_sample.shape[0]]
    c_neg_pred = c_neg_pred[c_neg_pred < ref_sample.shape[0]]

    c_tp = np.sum(ref_sample[c_pos_pred] == 1)
    c_fp = np.sum(ref_sample[c_pos_pred] == 0)

    c_tn = np.sum(ref_sample[c_neg_pred] == 0)
    c_fn = np.sum(ref_sample[c_neg_pred] == 1)

    c_precision = c_tp / (c_tp + c_fp)
    c_recall = c_tp / (c_tp + c_fn)
    c_f1 = _f1(c_precision, c_recall)

    # Compute word-level statistics

    # Find correctly tokenized words in the reference sample
    word_boundaries = _find_word_boudaries(ref_sample)

    # Find correctly tokenized words in the sample
    ss_boundaries = _find_word_boudaries(sample)
    tokenization_indicators = _find_words_correctly_tokenised(
        word_boundaries,
        ss_boundaries
    )

    correctly_tokenised_words = np.sum(tokenization_indicators)

    w_precision = correctly_tokenised_words / np.sum(sample)
    w_recall = correctly_tokenised_words / np.sum(ref_sample)
    w_f1 = _f1(w_precision, w_recall)

    tokenization_indicators = list(
        map(lambda x: str(x), tokenization_indicators)
    )

    return {
        'char_level': {
            'tp': c_tp,
            'fp': c_fp,
            'tn': c_tn,
            'fn': c_fn,
            'precision': c_precision,
            'recall': c_recall,
            'f1': c_f1
        },
        'word_level': {
            'precision':  w_precision,
            'recall':  w_recall,
            'f1': w_f1
        },
        'global': {
            'tokenisation_indicators': "".join(tokenization_indicators)
        }
    }


def _binary_representation(txt: str, verbose: bool = False):
    """
    Transform text to {0, 1} sequence

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
            print('%s -- %d' % (c, m))

    return bin_rept


def _find_word_boudaries(bin_reps) -> list:
    """
    Find start and end location of each word

    :param str bin_reps: binary representation of a text

    :return: list of tuples (start, end)
    :rtype: list[tuple(int, int)]
    """

    boundary = np.argwhere(bin_reps == 1).reshape(-1)
    start_idx = boundary
    end_idx = boundary[1:].tolist() + [bin_reps.shape[0]]

    return list(zip(start_idx, end_idx))


def _find_words_correctly_tokenised(
        ref_boundaries: list,
        predicted_boundaries: list
    ) -> tuple:
    """
    Find whether each word is correctly tokenized

    :param list[tuple(int, int)] ref_boundaries: word boundaries of reference tokenization
    :param list[tuple(int, int)] predicted_boundaries: word boundareies of predicted tokenization

    :return: binary sequence where 1 indicates the corresponding word is tokenized correctly
    :rtype: tuple[int] 
    """

    ref_b = dict(zip(ref_boundaries, [1]*len(ref_boundaries)))

    labels = tuple(map(lambda x: ref_b.get(x, 0), predicted_boundaries))
    return labels
