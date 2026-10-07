# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Word-level spelling correction using FastText-like embeddings."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Union, cast

from pythainlp.corpus import get_hf_hub
from pythainlp.tools.path import safe_path_join

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray
    from onnxruntime import InferenceSession


class FastTextEncoder:
    """
    FastText-like word encoder with ONNX nearest neighbor suggestions.

    This class loads pre-trained FastText-like word embeddings, computes
    word and sentence vectors, and interacts with an ONNX model for
    nearest neighbor suggestions.
    """

    model_dir: str
    nn_model_path: str
    bucket: int
    nb_words: int
    minn: int
    maxn: int
    vocabulary: list[str]
    embeddings: NDArray[np.float32]
    words_for_suggestion: NDArray[np.str_]
    nn_session: InferenceSession
    embedding_dim: int

    # --- Initialization and Data Loading ---

    def __init__(
        self,
        model_dir: str,
        nn_model_path: str,
        words_list: list[str],
        bucket: int = 2000000,
        nb_words: int = 2000000,
        minn: int = 5,
        maxn: int = 5,
    ) -> None:
        """
        Initialize the encoder.

        This method loads the embeddings, vocabulary, nearest neighbor
        model, and suggestion words list.

        :param str model_dir: directory containing ``embeddings.npy`` and
            ``vocabulary.txt``
        :param str nn_model_path: path to the ONNX nearest neighbor model
        :param list[str] words_list: list of words for suggestions
        :param int bucket: size of the hash bucket for subword hashing
        :param int nb_words: number of words in the vocabulary (used as an
            offset for subword indices)
        :param int minn: minimum length (in characters) of a subword
        :param int maxn: maximum length (in characters) of a subword
        :raises ModuleNotFoundError: if numpy or onnxruntime is not
            installed
        """
        try:
            import_module("numpy")
            import_module("onnxruntime")
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "Please install the required packages via "
                "'pip install numpy onnxruntime'."
            ) from exc
        self.model_dir = model_dir
        self.nn_model_path = nn_model_path
        self.bucket = bucket
        self.nb_words = nb_words
        self.minn = minn
        self.maxn = maxn

        # Load data and models
        self.vocabulary, self.embeddings = self._load_embeddings()
        self.words_for_suggestion = self._load_suggestion_words(words_list)
        self.nn_session = self._load_onnx_session(nn_model_path)
        self.embedding_dim = self.embeddings.shape[1]

    def _load_embeddings(self) -> tuple[list[str], NDArray[np.float32]]:
        """
        Load the embeddings matrix and vocabulary list.

        :return: vocabulary entries and their float32 embedding matrix
        :rtype: tuple[list[str], numpy.typing.NDArray[numpy.float32]]
        """
        import numpy as np

        input_matrix = np.load(
            safe_path_join(self.model_dir, "embeddings.npy"),
            allow_pickle=False,
        )
        vocab_path = safe_path_join(self.model_dir, "vocabulary.txt")
        with open(vocab_path, encoding="utf-8") as f:
            words = [line.rstrip() for line in f]
        return words, input_matrix

    def _load_suggestion_words(
        self, words_list: list[str]
    ) -> NDArray[np.str_]:
        """
        Load suggestion words into a NumPy string array.

        :param list[str] words_list: words for nearest neighbor lookup
        :return: words as a NumPy string array
        :rtype: numpy.typing.NDArray[numpy.str_]
        """
        import numpy as np

        words = np.array(words_list)
        return words

    def _load_onnx_session(self, onnx_path: str) -> InferenceSession:
        """
        Load the ONNX inference session.

        :param str onnx_path: path to the ONNX model
        :return: ONNX inference session
        :rtype: onnxruntime.InferenceSession
        """
        # Note: Using providers=["CPUExecutionProvider"] for platform independence
        import onnxruntime as rt

        sess = rt.InferenceSession(
            onnx_path, providers=["CPUExecutionProvider"]
        )
        return sess

    # --- Helper Methods for Encoding ---

    def _get_hash(self, subword: str) -> int:
        """
        Compute the FastText-like hash of a subword.

        :param str subword: subword to be hashed
        :return: hash value, offset by the number of words
        :rtype: int
        """
        h = 2166136261  # FNV-1a basis
        for c in subword:
            c_ord = ord(c) % 2**8
            h = (h ^ c_ord) % 2**32
            h = (h * 16777619) % 2**32  # FNV-1a prime
        return h % self.bucket + self.nb_words

    def _get_subwords(self, word: str) -> tuple[list[str], NDArray[np.int_]]:
        """
        Extract subwords and their corresponding integer indices.

        :param str word: word to extract subwords from
        :return: extracted subwords and their NumPy index array
        :rtype: tuple[list[str], numpy.typing.NDArray[numpy.int_]]
        """
        _word = "<" + word + ">"
        _subwords = []
        _subword_ids = []

        # 1. Check for the word in vocabulary (full word is the first subword)
        if word in self.vocabulary:
            _subwords.append(word)
            _subword_ids.append(self.vocabulary.index(word))
            if word == "</s>":
                import numpy as np

                return _subwords, np.array(_subword_ids)

        # 2. Extract n-grams (subwords) and get their hash indices
        for ngram_start in range(len(_word)):
            for ngram_length in range(self.minn, self.maxn + 1):
                if ngram_start + ngram_length <= len(_word):
                    _candidate_subword = _word[
                        ngram_start : ngram_start + ngram_length
                    ]
                    # Only append if not already included (e.g., as the full word)
                    if _candidate_subword not in _subwords:
                        _subwords.append(_candidate_subword)
                        _subword_ids.append(self._get_hash(_candidate_subword))

        import numpy as np

        return _subwords, np.array(_subword_ids)

    def get_word_vector(self, word: str) -> NDArray[np.float32]:
        """
        Compute the normalized vector for a single word.

        :param str word: word to be encoded
        :return: normalized float32 embedding vector
        :rtype: numpy.typing.NDArray[numpy.float32]
        """
        import numpy as np

        # subword_ids[1] contains the array of indices for the word and its subwords
        subword_ids = self._get_subwords(word)[1]

        # Check if the array of subword indices is empty
        if subword_ids.size == 0:
            # Return a 300-dimensional zero vector if no word/subword is found.
            return np.zeros(self.embedding_dim, dtype=np.float32)

        # Compute the mean of the embeddings for all subword indices
        vector = np.mean(
            [self.embeddings[s] for s in subword_ids],
            axis=0,
            dtype=np.float32,
        )

        # Normalize the vector
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm

        return cast("NDArray[np.float32]", vector)

    def _tokenize(self, sentence: str) -> list[str]:
        """
        Tokenize a sentence at whitespace.

        :param str sentence: sentence to be tokenized
        :return: list of words, with ``</s>`` added at each newline
        :rtype: list[str]
        """
        tokens = []
        word = ""
        for c in sentence:
            if c in [" ", "\n", "\r", "\t", "\v", "\f", "\0"]:
                if word:
                    tokens.append(word)
                    word = ""
                if c == "\n":
                    tokens.append("</s>")
            else:
                word += c
        if word:
            tokens.append(word)
        return tokens

    def get_sentence_vector(self, line: str) -> NDArray[np.float32]:
        """
        Compute the mean embedding vector for a sentence.

        :param str line: sentence to be encoded
        :return: float32 sentence embedding vector
        :rtype: numpy.typing.NDArray[numpy.float32]
        """
        import numpy as np

        tokens = self._tokenize(line)
        vectors = []
        for t in tokens:
            # get_word_vector already handles normalization, so no need to do it again here
            vec = self.get_word_vector(t)
            vectors.append(vec)

        # If the sentence was empty and resulted in no vectors, return a zero vector
        if not vectors:
            return np.zeros(self.embedding_dim, dtype=np.float32)

        return cast(
            "NDArray[np.float32]",
            np.mean(vectors, axis=0, dtype=np.float32),
        )

    # --- Nearest Neighbor Method ---

    def get_word_suggestion(
        self, list_word: Union[str, list[str]]
    ) -> Union[list[str], list[list[str]]]:
        """
        Find the nearest neighbor words of a word or a list of words.

        This method queries the ONNX model.

        :param Union[str, list[str]] list_word: word, or list of words,
            to get suggestions for
        :return: nearest neighbor words from the suggestion list, one list
            per input word; a single list if the input is a word
        :rtype: Union[list[str], list[list[str]]]
        """
        if isinstance(list_word, str):
            input_words = [list_word]
            return_single = True
        else:
            input_words = list_word
            return_single = False

        # Compute sentence vector for each input word/phrase
        # The original code's `get_sentence_vector(' '.join(list(word)))` seems
        # intended to treat a list of characters/tokens as a sentence.
        # I'll stick to a more standard usage: treat each item in `input_words`
        # as a separate phrase/word to encode.
        word_input_vecs = [
            self.get_sentence_vector(" ".join(list(word)))
            for word in input_words
        ]

        # Convert to numpy array for ONNX input (ensure float32)
        import numpy as np

        input_data = np.array(word_input_vecs, dtype=np.float32)

        # Run ONNX inference
        indices = self.nn_session.run(None, {"X": input_data})[0]

        # Look up suggestions
        suggestions = [self.words_for_suggestion[i].tolist() for i in indices]

        return suggestions[0] if return_single else suggestions


class Words_Spelling_Correction(FastTextEncoder):
    """Word-level spell checker and corrector using FastText."""

    model_name: str
    model_path: str
    model_onnx: str
    list_word: list[str]

    def __init__(self) -> None:
        """Initialize the word spelling correction model."""
        self.model_name = "pythainlp/word-spelling-correction-char2vec"
        self.model_path = get_hf_hub(self.model_name)
        self.model_onnx = get_hf_hub(self.model_name, "nearest_neighbors.onnx")
        with open(
            get_hf_hub(
                self.model_name, "list_word-spelling-correction-char2vec.txt"
            ),
            encoding="utf-8",
        ) as f:
            self.list_word = list(map(str.strip, f.readlines()))
        super().__init__(self.model_path, self.model_onnx, self.list_word)


_WSC_CACHE: dict[str, Words_Spelling_Correction] = {}


def get_words_spell_suggestion(
    list_words: Union[str, list[str]],
) -> Union[list[str], list[list[str]]]:
    """
    Get spelling suggestions for Thai words.

    This function retrieves spelling suggestions for one or more words.

    It requires numpy and onnxruntime. Install them before use.

    :param Union[str, list[str]] list_words: word, or list of words,
        to get suggestions for
    :return: spelling suggestions (at most 5 per word); a list of lists
        if the input is a list of words
    :rtype: Union[list[str], list[list[str]]]

    :Example:

        >>> from pythainlp.spell import (
        ...     get_words_spell_suggestion,
        ... )  # doctest: +SKIP

        >>> print(get_words_spell_suggestion("คมดี"))  # doctest: +SKIP
        ['คนดีผีคุ้ม', 'มีดคอม้า', 'คดี', 'มีดสองคม', 'มูลคดี']

        >>> print(
        ...     get_words_spell_suggestion(["คมดี", "กระเพาะ"])
        ... )  # doctest: +SKIP
        [['คนดีผีคุ้ม', 'มีดคอม้า', 'คดี', 'มีดสองคม', 'มูลคดี'],
        ['กระเพาะ', 'กระพา', 'กะเพรา', 'กระเพาะปลา', 'พระประธาน']]
    """
    if "default" not in _WSC_CACHE:
        _WSC_CACHE["default"] = Words_Spelling_Correction()
    return _WSC_CACHE["default"].get_word_suggestion(list_words)
