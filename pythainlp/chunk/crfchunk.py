# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""CRF-based Thai phrase structure (chunk) parser."""

from __future__ import annotations

from importlib.resources import as_file, files
from typing import TYPE_CHECKING, Any, Optional, Union, cast

if TYPE_CHECKING:
    import types
    from contextlib import AbstractContextManager

    from pycrfsuite import (
        Tagger as CRFTagger,  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[missing-module-attribute]
    )

from pythainlp.corpus import thai_stopwords


def _is_stopword(word: str) -> bool:
    return word in thai_stopwords()


def _doc2features(
    tokens: list[tuple[str, str]], index: int
) -> dict[str, Union[str, bool]]:
    """Extract features for a single token in a POS-tagged sentence.

    :param list[tuple[str, str]] tokens: POS-tagged sentence,
        a list of (word, POS-tag) pairs.
    :param int index: index of the token to extract features for.
    :return: feature dictionary for the token.
    :rtype: dict[str, Union[str, bool]]
    """
    word, pos = tokens[index]
    f: dict[str, Union[str, bool]] = {
        "word": word,
        "word_is_stopword": _is_stopword(word),
        "pos": pos,
    }
    if index > 1:
        prevprevword, prevprevpos = tokens[index - 2]
        f["prev-prev-word"] = prevprevword
        f["prev-prevz-word_is_stopword"] = _is_stopword(prevprevword)
        f["prev-prevz-pos"] = prevprevpos
    if index > 0:
        prevword, prevpos = tokens[index - 1]
        f["prev-word"] = prevword
        f["prev-word_is_stopword"] = _is_stopword(prevword)
        f["prev-pos"] = prevpos
    else:
        f["BOS"] = True
    if index < len(tokens) - 2:
        nextnextword, nextnextpos = tokens[index + 2]
        f["nextnext-word"] = nextnextword
        f["nextnext-word_is_stopword"] = _is_stopword(nextnextword)
        f["nextnext-pos"] = nextnextpos
    if index < len(tokens) - 1:
        nextword, nextpos = tokens[index + 1]
        f["next-word"] = nextword
        f["next-word_is_stopword"] = _is_stopword(nextword)
        f["next-pos"] = nextpos
    else:
        f["EOS"] = True

    return f


def _extract_features(
    doc: list[tuple[str, str]],
) -> list[dict[str, Union[str, bool]]]:
    return [_doc2features(doc, i) for i in range(len(doc))]


class CRFChunkParser:
    """CRF-based chunk parser for Thai text.

    Parses a POS-tagged sentence into phrase-structure chunks
    (IOB format), following the NLTK :class:`nltk.chunk.ChunkParserI`
    convention.

    This class supports the context manager protocol for deterministic
    resource cleanup:

    .. code-block:: python

        from pythainlp.chunk import CRFChunkParser

        with CRFChunkParser() as parser:
            result = parser.parse(tokens_pos)

    :param str corpus: corpus name for the CRF model
        (default: ``"orchidpp"``).
    """

    corpus: str
    _model_file_ctx: Optional[AbstractContextManager[Any]]
    tagger: CRFTagger
    xseq: list[dict[str, Union[str, bool]]]

    def __init__(self, corpus: str = "orchidpp") -> None:
        self.corpus = corpus
        self._model_file_ctx = None
        self.load_model(self.corpus)

    def load_model(self, corpus: str) -> None:
        """Load the CRF model for the given corpus.

        :param str corpus: corpus name.
        """
        from pycrfsuite import (
            Tagger as CRFTagger,  # noqa: PLC0415  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[missing-module-attribute]
        )

        self.tagger = CRFTagger()
        if corpus == "orchidpp":
            corpus_files = files("pythainlp.corpus")
            model_file = corpus_files.joinpath("crfchunk_orchidpp.model")
            self._model_file_ctx = as_file(model_file)
            model_path = self._model_file_ctx.__enter__()
            self.tagger.open(str(model_path))

    def parse(self, token_pos: list[tuple[str, str]]) -> list[str]:
        """Parse a POS-tagged sentence into IOB chunk labels.

        :param list[tuple[str, str]] token_pos: list of (word, POS-tag)
            pairs.
        :return: list of IOB chunk labels, one per token.
        :rtype: list[str]
        """
        self.xseq = _extract_features(token_pos)
        return cast(list[str], self.tagger.tag(self.xseq))

    def __enter__(self) -> CRFChunkParser:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        """Context manager exit — clean up resources."""
        if self._model_file_ctx is not None:
            try:
                self._model_file_ctx.__exit__(exc_type, exc_val, exc_tb)
                self._model_file_ctx = None
            except Exception:  # noqa: S110
                pass

    def __del__(self) -> None:
        """Attempt resource cleanup on garbage collection.

        .. note::
            :meth:`__del__` is not guaranteed to be called.
            Use the context manager protocol for reliable cleanup.
        """
        if self._model_file_ctx is not None:
            try:
                self._model_file_ctx.__exit__(None, None, None)
            except Exception:  # noqa: S110
                pass
