# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Evaluation metrics for Thai text generation tasks.

This module provides pure Python implementations of common evaluation
metrics (BLEU, ROUGE) that handle Thai text tokenization automatically.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import TYPE_CHECKING, Optional, TypedDict, Union, cast

from pythainlp.util.lcs import _lcs_lengths

if TYPE_CHECKING:
    from collections.abc import Sequence


class BleuScore(TypedDict):
    """BLEU score components returned by :func:`bleu_score`."""

    bleu: float  # BLEU score as a percentage (0.0 to 100.0)
    precisions: list[float]
    bp: float
    length_ratio: float
    hyp_length: int
    ref_length: int


class RougeScore(TypedDict):
    """Precision, recall, and F-measure for a single ROUGE type."""

    precision: float
    recall: float
    fmeasure: float


def _get_ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    """
    Get n-grams from a list of tokens.

    :param list[str] tokens: list of tokens
    :param int n: n-gram size

    :return: list of n-grams
    :rtype: list[tuple[str, ...]]
    """
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _calculate_precision_recall_fmeasure(
    overlap: int, hyp_count: int, ref_count: int
) -> tuple[float, float, float]:
    """
    Calculate precision, recall, and F-measure.

    :param int overlap: number of overlapping items
    :param int hyp_count: number of items in hypothesis
    :param int ref_count: number of items in reference

    :return: precision, recall, and F-measure
    :rtype: tuple[float, float, float]
    """
    precision = overlap / hyp_count if hyp_count > 0 else 0.0
    recall = overlap / ref_count if ref_count > 0 else 0.0

    if precision + recall > 0:
        fmeasure = 2 * precision * recall / (precision + recall)
    else:
        fmeasure = 0.0

    return precision, recall, fmeasure


def _lcs_length(x: Sequence[str], y: Sequence[str]) -> int:
    """
    Calculate the length of the longest common subsequence (LCS).

    :param Sequence[str] x: first sequence
    :param Sequence[str] y: second sequence

    :return: length of LCS
    :rtype: int
    """
    return _lcs_lengths(x, y)[len(x)][len(y)]


def _error_rate(ref: Sequence[str], hyp: Sequence[str]) -> float:
    """Calculate the edit distance divided by the reference length.

    :param Sequence[str] ref: reference items
    :param Sequence[str] hyp: hypothesis items

    :return: edit distance divided by ``len(ref)``; 0.0 if both are empty,
        infinity if only the reference is empty
    :rtype: float
    """
    r = len(ref)
    h = len(hyp)

    # d[i][j] is the edit distance between ref[:i] and hyp[:j]
    d = [[0] * (h + 1) for _ in range(r + 1)]
    for i in range(r + 1):
        d[i][0] = i
    for j in range(h + 1):
        d[0][j] = j

    for i in range(1, r + 1):
        for j in range(1, h + 1):
            if ref[i - 1] == hyp[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(
                    d[i - 1][j - 1] + 1,  # substitution
                    d[i][j - 1] + 1,  # insertion
                    d[i - 1][j] + 1,  # deletion
                )

    if r == 0:
        return 0.0 if h == 0 else float("inf")

    return d[r][h] / r


def _normalize_references(
    references: Union[list[str], list[list[str]]],
) -> list[list[str]]:
    """Wrap each reference in a list when one reference per hypothesis."""
    if references and isinstance(references[0], str):
        return [[ref] for ref in cast("list[str]", references)]
    return references  # type: ignore[return-value]


def _tokenize_text(text: str, tokenize: str, lowercase: bool) -> list[str]:
    """Tokenize a single text, optionally lowercasing the tokens."""
    from pythainlp.tokenize import word_tokenize

    tokens = word_tokenize(text, engine=tokenize, keep_whitespace=False)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


def _clipped_ngram_counts(
    hyp_tokens: list[str], ref_tokens_group: list[list[str]], n: int
) -> tuple[int, int]:
    """Count clipped hypothesis n-gram matches and all hypothesis n-grams."""
    hyp_ngrams = _get_ngrams(hyp_tokens, n)
    hyp_ngram_counts = Counter(hyp_ngrams)

    # Clip by the maximum count over all references
    max_ref_counts: Counter[tuple[str, ...]] = Counter()
    for ref_tokens in ref_tokens_group:
        ref_ngram_counts = Counter(_get_ngrams(ref_tokens, n))
        for ngram in ref_ngram_counts:
            max_ref_counts[ngram] = max(
                max_ref_counts[ngram], ref_ngram_counts[ngram]
            )

    clipped_count = 0
    for ngram, count in hyp_ngram_counts.items():
        clipped_count += min(count, max_ref_counts[ngram])
    return clipped_count, len(hyp_ngrams)


def _brevity_penalty(hyp_length: int, ref_length: int) -> float:
    """Calculate the BLEU brevity penalty."""
    if hyp_length == 0 and ref_length > 0:
        return 0.0
    if hyp_length < ref_length:
        return math.exp(1 - ref_length / hyp_length)
    return 1.0


def _ngram_precisions(
    clipped_counts: list[int],
    total_counts: list[int],
    max_ngram: int,
    smooth: bool,
) -> list[float]:
    """Calculate the n-gram precision for each n up to ``max_ngram``."""
    precisions = []
    for i in range(max_ngram):
        if total_counts[i] <= 0:
            precisions.append(0.0)
        elif smooth and clipped_counts[i] == 0:
            precisions.append(1.0 / (2 * total_counts[i]))
        else:
            precisions.append(clipped_counts[i] / total_counts[i])
    return precisions


def bleu_score(
    references: Union[list[str], list[list[str]]],
    hypotheses: list[str],
    tokenize: str = "newmm",
    lowercase: bool = False,
    max_ngram: int = 4,
    smooth: bool = True,
) -> BleuScore:
    """
    Calculate BLEU score for Thai text with automatic tokenization.

    This is a pure Python implementation of BLEU (Bilingual Evaluation
    Understudy) metric that automatically tokenizes Thai text using
    PyThaiNLP before calculating the score.

    :param Union[list[str], list[list[str]]] references: reference translations.
        Can be:
        - A list of strings (one reference per hypothesis)
        - A list of lists of strings (multiple references per hypothesis)
    :param list[str] hypotheses: hypothesis translations to evaluate
    :param str tokenize: tokenization engine to use (default: "newmm").
        See :func:`pythainlp.tokenize.word_tokenize` for available engines.
    :param bool lowercase: whether to lowercase text before evaluation
        (default: False)
    :param int max_ngram: maximum n-gram order (default: 4)
    :param bool smooth: whether to use smoothing for zero counts
        (default: True)

    :return: a :class:`BleuScore` typed dict with ``'bleu'``,
        ``'precisions'``, ``'bp'``, ``'length_ratio'``, ``'hyp_length'``,
        and ``'ref_length'``. ``'precisions'`` is ``list[float]``;
        ``'hyp_length'`` and ``'ref_length'`` are ``int``; all other
        values are ``float``.
    :rtype: BleuScore
    :raises ValueError: if the number of references and the number of
        hypotheses differ

    :Example:

        >>> from pythainlp.benchmarks import bleu_score

        >>> references = ["สวัสดีครับ วันนี้อากาศดีมาก"]
        >>> hypotheses = ["สวัสดีค่ะ วันนี้อากาศดี"]
        >>> score = bleu_score(references, hypotheses)
        >>> print(f"BLEU score: {score['bleu']:.2f}")
        BLEU score: 28.12

        >>> # Multiple references per hypothesis
        >>> references = [
        ...     ["สวัสดีครับ", "สวัสดีค่ะ"],  # two refs for first hypothesis
        ...     ["ลาก่อนครับ", "ลาก่อนค่ะ"],  # two refs for second hypothesis
        ... ]
        >>> hypotheses = ["สวัสดี", "ลาก่อน"]
        >>> score = bleu_score(references, hypotheses)
    """
    refs_normalized = _normalize_references(references)
    if len(refs_normalized) != len(hypotheses):
        raise ValueError(
            f"The number of references ({len(refs_normalized)}) and "
            f"hypotheses ({len(hypotheses)}) must be equal."
        )

    hyp_tokens_list = [
        _tokenize_text(hyp, tokenize, lowercase) for hyp in hypotheses
    ]
    refs_tokens_list = [
        [_tokenize_text(ref, tokenize, lowercase) for ref in refs]
        for refs in refs_normalized
    ]

    total_hyp_length = 0
    total_ref_length = 0
    clipped_counts = [0] * max_ngram
    total_counts = [0] * max_ngram

    for hyp_tokens, ref_tokens_group in zip(hyp_tokens_list, refs_tokens_list):
        total_hyp_length += len(hyp_tokens)

        # Find the reference length closest to hypothesis length
        ref_lengths = [len(ref) for ref in ref_tokens_group]
        closest_ref_len = min(
            ref_lengths, key=lambda ref_len: abs(ref_len - len(hyp_tokens))
        )
        total_ref_length += closest_ref_len

        for n in range(1, max_ngram + 1):
            clipped_count, total_count = _clipped_ngram_counts(
                hyp_tokens, ref_tokens_group, n
            )
            clipped_counts[n - 1] += clipped_count
            total_counts[n - 1] += total_count

    bp = _brevity_penalty(total_hyp_length, total_ref_length)
    precisions = _ngram_precisions(
        clipped_counts, total_counts, max_ngram, smooth
    )

    if all(p > 0 for p in precisions):
        log_precisions = [math.log(p) for p in precisions]
        geo_mean = math.exp(sum(log_precisions) / max_ngram)
        bleu = bp * geo_mean
    else:
        bleu = 0.0

    return BleuScore(
        bleu=bleu * 100,  # Return as percentage
        precisions=precisions,
        bp=bp,
        length_ratio=total_hyp_length / total_ref_length
        if total_ref_length > 0
        else 0.0,
        hyp_length=total_hyp_length,
        ref_length=total_ref_length,
    )


def rouge_score(
    reference: str,
    hypothesis: str,
    tokenize: str = "newmm",
    rouge_types: Optional[list[str]] = None,
) -> dict[str, RougeScore]:
    """
    Calculate ROUGE scores for Thai text with automatic tokenization.

    This is a pure Python implementation of ROUGE (Recall-Oriented
    Understudy for Gisting Evaluation) metric that automatically
    tokenizes Thai text using PyThaiNLP.

    Supported ROUGE types:
    - rouge1: unigram-based scoring
    - rouge2: bigram-based scoring
    - rougeL: longest common subsequence-based scoring

    :param str reference: reference text
    :param str hypothesis: hypothesis text to evaluate
    :param str tokenize: tokenization engine to use (default: "newmm").
        See :func:`pythainlp.tokenize.word_tokenize` for available engines.
    :param Optional[list[str]] rouge_types: list of ROUGE types to calculate.
        Default is ["rouge1", "rouge2", "rougeL"]

    :return: dictionary mapping ROUGE type to a :class:`RougeScore` typed dict
        with ``'precision'``, ``'recall'``, and ``'fmeasure'`` keys.
    :rtype: dict[str, RougeScore]

    :Example:

        >>> from pythainlp.benchmarks import rouge_score

        >>> reference = "สวัสดีครับ วันนี้อากาศดีมาก"
        >>> hypothesis = "สวัสดีค่ะ วันนี้อากาศดี"
        >>> scores = rouge_score(reference, hypothesis)
        >>> print(f"ROUGE-1 F-measure: {scores['rouge1']['fmeasure']:.4f}")
        ROUGE-1 F-measure: 0.6000
        >>> print(f"ROUGE-2 F-measure: {scores['rouge2']['fmeasure']:.4f}")
        ROUGE-2 F-measure: 0.2500
        >>> print(f"ROUGE-L F-measure: {scores['rougeL']['fmeasure']:.4f}")
        ROUGE-L F-measure: 0.6000
    """
    from pythainlp.tokenize import word_tokenize

    if rouge_types is None:
        rouge_types = ["rouge1", "rouge2", "rougeL"]

    ref_tokens = word_tokenize(
        reference, engine=tokenize, keep_whitespace=False
    )
    hyp_tokens = word_tokenize(
        hypothesis, engine=tokenize, keep_whitespace=False
    )

    result: dict[str, RougeScore] = {}

    for rouge_type in rouge_types:
        if rouge_type == "rouge1":
            ref_ngrams = Counter(ref_tokens)
            hyp_ngrams = Counter(hyp_tokens)

            overlap = sum((ref_ngrams & hyp_ngrams).values())
            ref_count = len(ref_tokens)
            hyp_count = len(hyp_tokens)

            precision, recall, fmeasure = _calculate_precision_recall_fmeasure(
                overlap, hyp_count, ref_count
            )
            result[rouge_type] = RougeScore(
                precision=precision, recall=recall, fmeasure=fmeasure
            )

        elif rouge_type == "rouge2":
            ref_bigrams = _get_ngrams(ref_tokens, 2)
            hyp_bigrams = _get_ngrams(hyp_tokens, 2)

            ref_bigram_counts = Counter(ref_bigrams)
            hyp_bigram_counts = Counter(hyp_bigrams)

            overlap = sum((ref_bigram_counts & hyp_bigram_counts).values())
            ref_count = len(ref_bigrams)
            hyp_count = len(hyp_bigrams)

            precision, recall, fmeasure = _calculate_precision_recall_fmeasure(
                overlap, hyp_count, ref_count
            )
            result[rouge_type] = RougeScore(
                precision=precision, recall=recall, fmeasure=fmeasure
            )

        elif rouge_type == "rougeL":
            lcs_len = _lcs_length(ref_tokens, hyp_tokens)
            ref_count = len(ref_tokens)
            hyp_count = len(hyp_tokens)

            precision, recall, fmeasure = _calculate_precision_recall_fmeasure(
                lcs_len, hyp_count, ref_count
            )
            result[rouge_type] = RougeScore(
                precision=precision, recall=recall, fmeasure=fmeasure
            )

    return result


def word_error_rate(
    reference: str,
    hypothesis: str,
    tokenize: str = "newmm",
) -> float:
    """
    Calculate Word Error Rate (WER) for Thai text with automatic tokenization.

    Word Error Rate is a common metric for evaluating speech recognition
    and machine translation systems. It measures the minimum number of
    word-level edits (insertions, deletions, substitutions) needed to
    transform the hypothesis into the reference, normalized by the
    reference length.

    WER = (S + D + I) / N

    where:
    - S = number of substitutions
    - D = number of deletions
    - I = number of insertions
    - N = number of words in reference

    :param str reference: reference text
    :param str hypothesis: hypothesis text to evaluate
    :param str tokenize: tokenization engine to use (default: "newmm").
        See :func:`pythainlp.tokenize.word_tokenize` for available engines.

    :return: word error rate as a float (0.0 = perfect, >1.0 = very poor)
    :rtype: float

    :Example:

        >>> from pythainlp.benchmarks import word_error_rate

        >>> reference = "สวัสดีครับ วันนี้อากาศดีมาก"
        >>> hypothesis = "สวัสดีค่ะ วันนี้อากาศดี"
        >>> wer = word_error_rate(reference, hypothesis)
        >>> print(f"WER: {wer:.4f}")
        WER: 0.4000
    """
    from pythainlp.tokenize import word_tokenize

    ref_tokens = word_tokenize(
        reference, engine=tokenize, keep_whitespace=False
    )
    hyp_tokens = word_tokenize(
        hypothesis, engine=tokenize, keep_whitespace=False
    )

    return _error_rate(ref_tokens, hyp_tokens)


def character_error_rate(
    reference: str,
    hypothesis: str,
) -> float:
    """
    Calculate Character Error Rate (CER) for Thai text.

    Character Error Rate is a metric for evaluating speech recognition
    and optical character recognition (OCR) systems. It measures the
    minimum number of character-level edits (insertions, deletions,
    substitutions) needed to transform the hypothesis into the reference,
    normalized by the reference length.

    CER = (S + D + I) / N

    where:
    - S = number of substitutions
    - D = number of deletions
    - I = number of insertions
    - N = number of characters in reference

    :param str reference: reference text
    :param str hypothesis: hypothesis text to evaluate

    :return: character error rate as a float (0.0 = perfect, >1.0 = very poor)
    :rtype: float

    :Example:

        >>> from pythainlp.benchmarks import character_error_rate

        >>> reference = "สวัสดีครับ"
        >>> hypothesis = "สวัสดีค่ะ"
        >>> cer = character_error_rate(reference, hypothesis)
        >>> print(f"CER: {cer:.4f}")
        CER: 0.3000
    """
    ref_chars = list(reference)
    hyp_chars = list(hypothesis)

    return _error_rate(ref_chars, hyp_chars)
