# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import types
from contextlib import AbstractContextManager
from importlib.resources import as_file, files
from typing import Any, Optional

from pycrfsuite import Tagger as CRFTagger

from pythainlp.corpus import thai_stopwords


def _is_stopword(word: str) -> bool:  # check Thai stopword
    return word in thai_stopwords()


def _doc2features(tokens: list[tuple[str, str]], index: int) -> dict[str, Any]:
    """`tokens` = a POS-tagged sentence [(w1, t1), ...]
    `index` = the index of the token we want to extract features for
    """
    word, pos = tokens[index]
    f: dict[str, Any] = {
        "word": word,
        "word_is_stopword": _is_stopword(word),
        "pos": pos,
    }
    if index > 0 and index > 1:
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


def extract_features(doc: list[tuple[str, str]]) -> list[dict[str, Any]]:
    return [_doc2features(doc, i) for i in range(0, len(doc))]


class CRFchunk:
    """CRF-based chunker for Thai text.

    This class can be used as a context manager to ensure proper cleanup
    of resources. Example:

        with CRFchunk() as chunker:
            result = chunker.parse(tokens)

    Alternatively, the object will attempt to clean up resources when
    garbage collected, though this is not guaranteed.
    """

    corpus: str
    _model_file_ctx: Optional[AbstractContextManager[Any]]
    tagger: CRFTagger
    xseq: list[dict[str, Any]]

    def __init__(self, corpus: str = "orchidpp") -> None:
        self.corpus: str = corpus
        self._model_file_ctx: Optional[AbstractContextManager[Any]] = None
        self.load_model(self.corpus)

    def load_model(self, corpus: str) -> None:
        self.tagger: CRFTagger = CRFTagger()
        if corpus == "orchidpp":
            corpus_files = files("pythainlp.corpus")
            model_file = corpus_files.joinpath("crfchunk_orchidpp.model")
            self._model_file_ctx: Optional[AbstractContextManager[Any]] = (
                as_file(model_file)
            )
            model_path = self._model_file_ctx.__enter__()
            self.tagger.open(str(model_path))

    def parse(self, token_pos: list[tuple[str, str]]) -> list[str]:
        self.xseq: list[dict[str, Any]] = extract_features(token_pos)
        return self.tagger.tag(self.xseq)  # type: ignore[no-any-return]

    def __enter__(self) -> CRFchunk:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        """Context manager exit - clean up resources."""
        if self._model_file_ctx is not None:
            try:
                self._model_file_ctx.__exit__(exc_type, exc_val, exc_tb)
                self._model_file_ctx = None
            except Exception:  # noqa: S110
                pass

    def __del__(self) -> None:
        """Clean up the context manager when object is destroyed.

        Note: __del__ is not guaranteed to be called and should not be
        relied upon for critical cleanup. Use the context manager protocol
        (with statement) for reliable resource management.
        """
        if self._model_file_ctx is not None:
            try:
                self._model_file_ctx.__exit__(None, None, None)
            except Exception:  # noqa: S110
                # Silently ignore cleanup errors during garbage collection
                pass
