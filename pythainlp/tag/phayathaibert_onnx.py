# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""PhayaThaiBERT part-of-speech tagger with ONNX Runtime backend.

The model is an ONNX export of
`nlp-chula/phayathaibert-thai-pos-tagger
<https://huggingface.co/nlp-chula/phayathaibert-thai-pos-tagger>`_,
fine-tuned on the UD Thai-TUD treebank. It tags words with Universal POS tags.
"""

from __future__ import annotations

import json
import threading
import unicodedata
from collections import Counter
from typing import TYPE_CHECKING, Optional

from pythainlp.corpus import get_hf_hub

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from onnxruntime import InferenceSession
    from tokenizers import Encoding, Tokenizer

_REPO_ID = "wiriyabot/phayathaibert-thai-pos-tagger-onnx"
# Pinned for reproducible and secure downloads.
_REVISION = "ff55e2c66ef22deee18c423cee272f6e207171ae"

# Maximum number of subword tokens the model accepts, including <s> and </s>.
_MAX_SEQUENCE_LENGTH = 510

# Tag for words the model never sees (whitespace-only words), matching
# the perceptron tagger with Universal POS corpora.
_WHITESPACE_TAG = "PUNCT"

# Universal POS tag for words that produce no subword token.
_UNKNOWN_TAG = "X"


def _is_blank(word: str) -> bool:
    """Return True if a word has only whitespace or format characters.

    Format characters (Unicode category Cf) include the zero-width space,
    zero-width non-joiner and byte order mark, which carry no text.

    :param str word: a word
    :return: whether the word is empty, whitespace or format characters
    :rtype: bool
    """
    return all(ch.isspace() or unicodedata.category(ch) == "Cf" for ch in word)


def _first_subword_labels(
    word_ids: Sequence[Optional[int]],
    label_ids: Sequence[int],
    n_words: int,
    id2label: Mapping[int, str],
) -> list[str]:
    """Pick each word's tag from the prediction for its first subword.

    This is the alignment the model was trained with.

    :param word_ids: word index of each subword token; ``None`` for special
        tokens
    :param label_ids: predicted label id of each subword token
    :param n_words: number of input words
    :param id2label: mapping from label id to tag name
    :return: one tag per word; ``"X"`` for a word that produced no subword
    :rtype: list[str]
    """
    tags = [_UNKNOWN_TAG] * n_words
    seen: set[int] = set()
    for word_id, label_id in zip(word_ids, label_ids):
        if word_id is None or word_id in seen:
            continue
        seen.add(word_id)
        tags[word_id] = id2label[label_id]
    return tags


def _chunk_spans(
    subword_counts: Sequence[int], max_subwords: int
) -> list[tuple[int, int]]:
    """Group consecutive words into spans that fit the model's input length.

    A word longer than ``max_subwords`` gets a span of its own; its subwords
    are truncated at encoding time, which keeps its first subword.

    :param subword_counts: number of subword tokens of each word
    :param max_subwords: maximum number of subword tokens per span
    :return: ``(start, end)`` word index pairs, end exclusive
    :rtype: list[tuple[int, int]]
    """
    spans: list[tuple[int, int]] = []
    start = 0
    total = 0
    for i, count in enumerate(subword_counts):
        if i > start and total + count > max_subwords:
            spans.append((start, i))
            start = i
            total = 0
        total += count
    if subword_counts:
        spans.append((start, len(subword_counts)))
    return spans


class PhayaThaiBERTTagger:
    """Universal POS tagger using PhayaThaiBERT with ONNX Runtime.

    Requires ``numpy``, ``onnxruntime``, ``tokenizers`` and
    ``huggingface-hub``. The model (about 530 MB) is downloaded from
    the Hugging Face Hub on first use.

    :param str repo_id: Hugging Face Hub repository of the ONNX model
    :param Optional[str] revision: git revision of the repository.
        The default repository is pinned to a commit when this is ``None``.
    """

    session: InferenceSession
    tokenizer: Tokenizer
    id2label: dict[int, str]

    def __init__(
        self, repo_id: str = _REPO_ID, revision: Optional[str] = None
    ) -> None:
        try:
            import huggingface_hub  # noqa: F401
            import numpy  # noqa: F401
            from onnxruntime import InferenceSession
            from tokenizers import Tokenizer
        except ImportError as e:
            raise ImportError(
                "PhayaThaiBERT POS tagger requires numpy, onnxruntime,"
                " tokenizers and huggingface-hub."
                ' Install them with: pip install "pythainlp[phayathaibert_onnx]"'
            ) from e

        if revision is None and repo_id == _REPO_ID:
            revision = _REVISION
        model_path = get_hf_hub(repo_id, "model.onnx", revision=revision)
        tokenizer_path = get_hf_hub(
            repo_id, "tokenizer.json", revision=revision
        )
        config_path = get_hf_hub(repo_id, "config.json", revision=revision)

        self.session = InferenceSession(
            model_path, providers=["CPUExecutionProvider"]
        )
        self.tokenizer = Tokenizer.from_file(tokenizer_path)
        # tokenizer.json ships with truncation at 510 tokens, which would
        # silently drop words; chunking is done here instead.
        self.tokenizer.no_truncation()
        self.tokenizer.no_padding()
        with open(config_path, encoding="utf-8") as f:
            self.id2label = {
                int(k): v for k, v in json.load(f)["id2label"].items()
            }

    def tag(self, words: list[str]) -> list[tuple[str, str]]:
        """Tag a list of words with Universal POS tags.

        Words with only whitespace or format characters (such as the
        zero-width space) are tagged ``PUNCT`` without being passed to the
        model. Input longer than the model limit is tagged in consecutive
        chunks of whole words.

        :param list[str] words: a list of tokenized words
        :return: a list of tuples (word, POS tag)
        :rtype: list[tuple[str, str]]
        """
        tags = [_WHITESPACE_TAG] * len(words)
        positions = [i for i, word in enumerate(words) if not _is_blank(word)]
        content = [words[i] for i in positions]
        if content:
            for position, tag in zip(positions, self._tag_content(content)):
                tags[position] = tag
        return list(zip(words, tags))

    def _tag_content(self, words: list[str]) -> list[str]:
        encoding = self.tokenizer.encode(words, is_pretokenized=True)
        if len(encoding.ids) <= _MAX_SEQUENCE_LENGTH:
            return self._predict(encoding, len(words))

        counts = Counter(i for i in encoding.word_ids if i is not None)
        subword_counts = [counts.get(i, 0) for i in range(len(words))]
        labels: list[str] = []
        # Two positions are taken by <s> and </s>.
        for start, end in _chunk_spans(
            subword_counts, _MAX_SEQUENCE_LENGTH - 2
        ):
            chunk = words[start:end]
            chunk_encoding = self.tokenizer.encode(chunk, is_pretokenized=True)
            labels.extend(self._predict(chunk_encoding, len(chunk)))
        return labels

    def _predict(self, encoding: Encoding, n_words: int) -> list[str]:
        import numpy as np

        ids = encoding.ids
        mask = encoding.attention_mask
        word_ids = encoding.word_ids
        if len(ids) > _MAX_SEQUENCE_LENGTH:
            # Only a single over-long word gets here; its first subword stays.
            ids = ids[: _MAX_SEQUENCE_LENGTH - 1] + ids[-1:]
            mask = mask[:_MAX_SEQUENCE_LENGTH]
            word_ids = word_ids[: _MAX_SEQUENCE_LENGTH - 1] + [None]
        logits = self.session.run(
            None,
            {
                "input_ids": np.array([ids], dtype=np.int64),
                "attention_mask": np.array([mask], dtype=np.int64),
            },
        )[0][0]
        return _first_subword_labels(
            word_ids, logits.argmax(axis=-1).tolist(), n_words, self.id2label
        )


_TAGGER: Optional[PhayaThaiBERTTagger] = None
_TAGGER_LOCK = threading.Lock()


def tag(words: list[str], corpus: str = "tud") -> list[tuple[str, str]]:
    """Tag words with Universal POS tags using PhayaThaiBERT (ONNX).

    :param list[str] words: a list of tokenized words
    :param str corpus: ignored; the model is trained on UD Thai-TUD only
    :return: a list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]
    """
    global _TAGGER
    if not words:
        return []
    if _TAGGER is None:
        with _TAGGER_LOCK:
            if _TAGGER is None:
                _TAGGER = PhayaThaiBERTTagger()
    return _TAGGER.tag(words)
