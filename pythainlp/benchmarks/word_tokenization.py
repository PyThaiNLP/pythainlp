# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""Benchmark metrics for word tokenization."""

from __future__ import annotations

import operator
import re
import sys

# Runtime import keeps typing.get_type_hints() working on this module.
from collections.abc import Mapping  # noqa: TC003
from itertools import accumulate
from typing import (
    TYPE_CHECKING,
    Any,
    NamedTuple,
    TypedDict,
    Union,
    cast,
    overload,
)

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd
    from numpy.typing import NDArray

__all__: list[str] = [
    "CharLevelStat",
    "GlobalStat",
    "TokenizationScore",
    "TokenizationStat",
    "WordLevelStat",
    "benchmark",
    "char_eval_function",
    "compute_stats",
    "evaluate_word_tokenization",
    "preprocessing",
    "word_eval_function",
]

SEPARATOR: str = "|"

# regex for removing one space surrounded by separators, i.e. | |
SURROUNDING_SEPS_RX: re.Pattern[str] = re.compile(
    "{sep}? ?{sep}$".format(sep=re.escape(SEPARATOR))
)

# regex for removing repeated separators, i.e. ||||
MULTIPLE_SEPS_RX: re.Pattern[str] = re.compile(f"{re.escape(SEPARATOR)}+")

# regex for removing tags, i.e. <NE>, </NE>
TAG_RX: re.Pattern[str] = re.compile(r"<\/?[A-Z]+>")

# regex for removing trailing separators, i.e.  a|dog| -> a|dog
TAILING_SEP_RX: re.Pattern[str] = re.compile(f"{re.escape(SEPARATOR)}$")


class CharLevelStat(TypedDict):
    """Character-level confusion matrix statistics for tokenization."""

    tp: int
    fp: int
    tn: int
    fn: int


class WordLevelStat(TypedDict):
    """Word-level tokenization statistics."""

    correctly_tokenized_words: int
    total_words_in_sample: int
    total_words_in_ref_sample: int


class GlobalStat(TypedDict):
    """Global tokenization indicator as a binary indicator string."""

    tokenization_indicators: str


class TokenizationStat(TypedDict):
    """Tokenization quality statistics at character, word, and global level."""

    char_level: CharLevelStat
    word_level: WordLevelStat
    global_: GlobalStat


class TokenizationScore(NamedTuple):
    """Tokenization evaluation score containing character and word scores."""

    char_score: float
    word_score: float


def _f1(precision: float, recall: float) -> float:
    """
    Compute the F1 score.

    :param float precision: precision value
    :param float recall: recall value

    :return: F1 score
    :rtype: float
    """
    if precision == recall == 0:
        return 0
    return 2 * precision * recall / (precision + recall)


@overload
def _flatten_result(
    my_dict: TokenizationStat, sep: str = ...
) -> dict[str, Union[int, str]]: ...


@overload
def _flatten_result(
    my_dict: Mapping[str, Mapping[str, Union[int, str]]], sep: str = ...
) -> dict[str, Union[int, str]]: ...


def _flatten_result(
    my_dict: Any,
    sep: str = ":",
) -> dict[str, Union[int, str]]:
    """
    Flatten a two-level dictionary.

    Uses keys from the first level as a prefix for keys in the second level.
    For example::

        my_dict = {"a": {"b": 7}}
        _flatten_result(my_dict)
        # {"a:b": 7}

    :param my_dict: dictionary containing statistics
    :type my_dict: TokenizationStat or
        collections.abc.Mapping[str,
        collections.abc.Mapping[str, Union[int, str]]]
    :param str sep: separator between the two keys (default is ``":"``)

    :return: flat dictionary with combined keys
    :rtype: dict[str, Union[int, str]]
    """
    return {
        f"{k1}{sep}{k2}": v
        for k1, kv2 in my_dict.items()
        for k2, v in kv2.items()
    }


def benchmark(ref_samples: list[str], samples: list[str]) -> pd.DataFrame:
    """
    Benchmark tokenized samples against reference samples.

    See :func:`pythainlp.benchmarks.word_tokenization.compute_stats`
    for computed metrics.

    :param list[str] ref_samples: reference (ground truth) samples
    :param list[str] samples: samples to evaluate

    :return: dataframe with shape ``len(samples) × len(metrics)``
    :rtype: pandas.DataFrame
    """
    import pandas as pd

    results = []
    for i, (r, s) in enumerate(zip(ref_samples, samples)):
        try:
            r, s = preprocessing(r), preprocessing(s)  # noqa: PLW2901
            if r and s:
                stats = compute_stats(r, s)
                flat_stats: dict[str, Union[int, str]] = _flatten_result(stats)
                flat_stats["expected"] = r
                flat_stats["actual"] = s
                results.append(flat_stats)
        except Exception as exc:
            reason = f"""
[Error]
Reason: {sys.exc_info()}

Pair (i={i})
--- label
{r}
--- sample
{s}
"""
            raise SystemExit(reason) from exc

    return pd.DataFrame(results)


def preprocessing(txt: str, remove_space: bool = True) -> str:
    # TODO: docstring names ``text``, but the parameter is ``txt``
    """
    Clean up text before performing evaluation.

    :param str text: text to preprocess
    :param bool remove_space: remove white space

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


def compute_stats(ref_sample: str, raw_sample: str) -> TokenizationStat:
    """
    Compute statistics for tokenization quality.

    These statistics include:

    * *Character-level* - true positive, false positive, true negative,
      false negative
    * *Word-level* - precision, recall, and F1
    * *Global* - a ``{0, 1}`` sequence indicating whether each word
      is tokenized correctly

    :param str ref_sample: reference (ground truth) sample
    :param str raw_sample: sample to evaluate

    :return: character-level, word-level, and global tokenization metrics
    :rtype: TokenizationStat
    """
    import numpy as np

    ref_sample_arr = _binary_representation(ref_sample)
    sample_arr = _binary_representation(raw_sample)

    # Compute character-level statistics
    c_pos_pred, c_neg_pred = (
        np.argwhere(sample_arr == 1),
        np.argwhere(sample_arr == 0),
    )

    c_pos_pred = c_pos_pred[c_pos_pred < ref_sample_arr.shape[0]]
    c_neg_pred = c_neg_pred[c_neg_pred < ref_sample_arr.shape[0]]

    c_tp: int = int(np.sum(ref_sample_arr[c_pos_pred] == 1))
    c_fp: int = int(np.sum(ref_sample_arr[c_pos_pred] == 0))

    c_tn: int = int(np.sum(ref_sample_arr[c_neg_pred] == 0))
    c_fn: int = int(np.sum(ref_sample_arr[c_neg_pred] == 1))

    # Compute word-level statistics

    # Find correctly tokenized words in the reference sample
    word_boundaries = _find_word_boundaries(ref_sample_arr)

    # Find correctly tokenized words in the sample
    ss_boundaries = _find_word_boundaries(sample_arr)
    tokenization_indicators = _find_words_correctly_tokenized(
        word_boundaries, ss_boundaries
    )

    correctly_tokenized_words: int = int(np.sum(tokenization_indicators))

    tokenization_indicators_str = list(map(str, tokenization_indicators))

    return {
        "char_level": CharLevelStat(
            tp=c_tp,
            fp=c_fp,
            tn=c_tn,
            fn=c_fn,
        ),
        "word_level": WordLevelStat(
            correctly_tokenized_words=correctly_tokenized_words,
            total_words_in_sample=int(np.sum(sample_arr)),
            total_words_in_ref_sample=int(np.sum(ref_sample_arr)),
        ),
        "global_": GlobalStat(
            tokenization_indicators="".join(tokenization_indicators_str),
        ),
    }


def _binary_representation(
    txt: str, verbose: bool = False
) -> NDArray[np.int8]:
    """
    Transform text into a {0, 1} sequence.

    A 1 indicates that the corresponding character is the beginning of
    a word. For example, ผม|ไม่|ชอบ|กิน|ผัก -> 10100...

    :param str txt: text to transform
    :param bool verbose: print each character with its value, for debugging

    :return: {0, 1} sequence
    :rtype: numpy.typing.NDArray[numpy.int8]
    """
    import numpy as np

    chars = np.array(list(txt))

    boundary = np.argwhere(chars == SEPARATOR).reshape(-1)
    boundary = boundary - np.array(range(boundary.shape[0]))

    bin_rept = np.zeros(len(txt) - boundary.shape[0], dtype=np.int8)
    bin_rept[[*list(boundary), 0]] = 1

    sample_wo_seps = list(txt.replace(SEPARATOR, ""))

    # sanity check
    if len(sample_wo_seps) != len(bin_rept):
        raise ValueError(
            f"Length mismatch: sample_wo_seps={len(sample_wo_seps)}, "
            f"bin_rept={len(bin_rept)}"
        )

    if verbose:
        for c, m in zip(sample_wo_seps, bin_rept):
            print(f"{c} -- {m}")

    return bin_rept


def _find_word_boundaries(
    bin_reps: NDArray[np.int8],
) -> list[tuple[int, int]]:
    """
    Find the starting and ending location of each word.

    :param numpy.typing.NDArray[numpy.int8] bin_reps: binary representation
        of a text

    :return: list of tuples (start, end)
    :rtype: list[tuple[int, int]]
    """
    import numpy as np

    boundary = np.argwhere(bin_reps == 1).reshape(-1)
    start_idx = boundary
    end_idx = [*boundary[1:].tolist(), bin_reps.shape[0]]

    return list(zip(start_idx, end_idx))


def _find_words_correctly_tokenized(
    ref_boundaries: list[tuple[int, int]],
    predicted_boundaries: list[tuple[int, int]],
) -> tuple[int, ...]:
    """
    Find whether each word is correctly tokenized.

    :param list[tuple[int, int]] ref_boundaries: word boundaries of
        the reference tokenization
    :param list[tuple[int, int]] predicted_boundaries: word boundaries of
        the predicted tokenization

    :return: binary sequence; 1 means the word is tokenized correctly
    :rtype: tuple[int, ...]
    """
    ref_b = dict(zip(ref_boundaries, [1] * len(ref_boundaries)))

    labels = tuple(ref_b.get(x, 0) for x in predicted_boundaries)
    return labels


def char_eval_function(
    y_true: Union[list[int], tuple[int, ...]],
    y_pred: Union[list[int], tuple[int, ...]],
) -> float:
    """
    Compute the character-level F1 score for boundary indicators.

    Calculate precision, recall, and binary F1 score for boundary (1)
    labels between reference and predicted character boundary sequences.
    Ported from SEFR CUT (``sefr_cut.evaluation``).

    :param y_true: reference (ground truth) binary boundary sequence
    :type y_true: Union[list[int], tuple[int, ...]]
    :param y_pred: predicted binary boundary sequence
    :type y_pred: Union[list[int], tuple[int, ...]]

    :return: character-level F1 score
    :rtype: float
    """
    min_len: int = min(len(y_true), len(y_pred))
    tp: int = sum(y_true[i] == 1 and y_pred[i] == 1 for i in range(min_len))
    fp: int = sum(y_true[i] == 0 and y_pred[i] == 1 for i in range(min_len))
    fn: int = sum(y_true[i] == 1 and y_pred[i] == 0 for i in range(min_len))

    if len(y_pred) > min_len:
        fp += sum(y_pred[i] == 1 for i in range(min_len, len(y_pred)))
    if len(y_true) > min_len:
        fn += sum(y_true[i] == 1 for i in range(min_len, len(y_true)))

    if tp == 0:
        return 0.0

    precision: float = tp / (tp + fp)
    recall: float = tp / (tp + fn)
    return _f1(precision, recall)


def word_eval_function(
    train: list[str],
    test: list[str],
) -> float:
    """
    Compute the word-level F1 score for lists of words.

    Calculate the F1 score based on word boundary span overlap between
    the reference (ground truth) words and the predicted words.
    Ported from SEFR CUT (``sefr_cut.evaluation``).

    :param list[str] train: reference (ground truth) list of words
    :param list[str] test: predicted list of words

    :return: word-level F1 score
    :rtype: float
    """
    if not train or not test:
        return 0.0

    train_acc = list(accumulate(map(len, train), func=operator.add))
    test_acc = list(accumulate(map(len, test), func=operator.add))
    train_set = set(zip([0, *train_acc], train_acc))
    test_set = set(zip([0, *test_acc], test_acc))
    correct: int = len(train_set & test_set)

    if correct == 0:
        return 0.0

    precision: float = correct / len(test)
    recall: float = correct / len(train)
    return _f1(precision, recall)


def _preprocess_attacut(
    sentence_lines: list[str],
) -> tuple[list[str], list[list[int]]]:
    """
    Convert segmented sentences to text and binary boundary indicators.

    Adapted from SEFR CUT preprocessing.

    :param list[str] sentence_lines: list of segmented sentences
        containing separators (``"|"``)

    :return: tuple of (list of texts, list of binary label lists)
    :rtype: tuple[list[str], list[list[int]]]
    """
    x: list[str] = []
    y: list[list[int]] = []
    for sentence in sentence_lines:
        x.append(sentence.replace(SEPARATOR, ""))
        padded = SEPARATOR + sentence
        y_char: list[int] = []
        for idx in range(1, len(padded)):
            current_char = padded[idx]
            before_char = padded[idx - 1]

            if current_char == SEPARATOR:
                continue

            target = 1 if before_char == SEPARATOR else 0
            y_char.append(target)
        y.append(y_char)

    return x, y


def _normalize_evaluation_input(
    x: Union[str, list[str], list[list[str]]],
    sep: str = "",
) -> list[str]:
    """
    Normalize evaluation input into a list containing a single string.

    Handle a string, a list of strings, or a list of lists of strings.

    :param x: text or tokens
    :type x: Union[str, list[str], list[list[str]]]
    :param str sep: separator to join tokens or sentences
        (default is ``""``)

    :return: list containing a single concatenated string
    :rtype: list[str]
    :raises TypeError: if ``x`` is not a string or a list
    """
    if isinstance(x, str):
        return [x]

    if not isinstance(x, list):
        raise TypeError(
            f"Input must be a string, list of strings, or list of list of "
            f"strings, got {type(x).__name__}"
        )

    if len(x) == 0:
        return [""]

    if isinstance(x[0], list):
        nested = cast("list[list[str]]", x)
        flat: list[str] = [j for sub in nested for j in sub]
        return [f"{sep}".join(flat)]

    tokens = cast("list[str]", x)

    if len(tokens) == 1 and isinstance(tokens[0], str):
        return tokens

    if sep:
        return [f"{sep}".join(tokens)]

    return ["".join(tokens)]


def evaluate_word_tokenization(
    x_true: Union[str, list[str], list[list[str]]],
    x_pred: Union[str, list[str], list[list[str]]],
    sep: str = "",
) -> TokenizationScore:
    """
    Evaluate word tokenization at character and word levels.

    Compute the character-level F1 score and the word-level F1 score
    between the reference (``x_true``) and predicted (``x_pred``)
    segmentation. Ported from SEFR CUT (``sefr_cut.evaluation``).

    Supported input representations:

    * strings delimited by ``"|"``, such as ``"สวัสดี|ประเทศไทย"``
    * single-element lists of delimited strings, such as
      ``["สวัสดี|ประเทศไทย"]``
    * 2D lists of strings, such as ``[["สวัสดี|"], ["ประเทศไทย"]]``
    * 1D lists of tokens with ``sep="|"``, such as
      ``["สวัสดี", "ประเทศไทย"]``

    :param x_true: reference (ground truth) text or tokens
    :type x_true: Union[str, list[str], list[list[str]]]
    :param x_pred: predicted text or tokens
    :type x_pred: Union[str, list[str], list[list[str]]]
    :param str sep: separator to join sub-elements when the input is a
        list of tokens without boundaries (default is ``""``)

    :return: tokenization score containing character score and word score
    :rtype: TokenizationScore

    :Example:
    ::

        from pythainlp.benchmarks import evaluate_word_tokenization

        answer = "สวัสดี|ประเทศไทย"
        pred = "สวัสดี|ประเทศ|ไทย"
        char_score, word_score = evaluate_word_tokenization(answer, pred)
        print(f"Char Score: {char_score}, Word Score: {word_score}")
        # Char Score: 0.8, Word Score: 0.4
    """
    x_true_1d: list[str] = _normalize_evaluation_input(x_true, sep=sep)
    x_pred_1d: list[str] = _normalize_evaluation_input(x_pred, sep=sep)

    _, y_true_boolean = _preprocess_attacut(x_true_1d)
    _, y_pred_boolean = _preprocess_attacut(x_pred_1d)

    char_score: float = 0.0
    if y_true_boolean and y_pred_boolean:
        char_score = char_eval_function(y_true_boolean[0], y_pred_boolean[0])

    true_words: list[str] = [w for w in x_true_1d[0].split(SEPARATOR) if w]
    pred_words: list[str] = [w for w in x_pred_1d[0].split(SEPARATOR) if w]
    word_score: float = word_eval_function(true_words, pred_words)

    return TokenizationScore(char_score=char_score, word_score=word_score)
