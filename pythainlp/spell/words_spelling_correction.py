# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
import os
from pythainlp.corpus import get_hf_hub
from typing import List, Union


class FastTextEncoder:
    """
    A class to load pre-trained FastText-like word embeddings, 
    compute word and sentence vectors, and interact with an ONNX 
    model for nearest neighbor suggestions.
    """

    # --- Initialization and Data Loading ---
    
    def __init__(self, model_dir, nn_model_path, words_list, bucket=2000000, nb_words=2000000, minn=5, maxn=5):
        """
        Initializes the FastTextEncoder, loading embeddings, vocabulary, 
        nearest neighbor model, and suggestion words list.

        Args:
            model_dir (str): Directory containing 'embeddings.npy' and 'vocabulary.txt'.
            nn_model_path (str): Path to the ONNX nearest neighbors model.
            words_list (str): the list of words for suggestions.
            bucket (int): The size of the hash bucket for subword hashing.
            nb_words (int): The number of words in the vocabulary (used as an offset for subword indices).
            minn (int): Minimum character length for subwords.
            maxn (int): Maximum character length for subwords.
        """
        try:
            import numpy as np # reduce load
            import onnxruntime
            self.np = np
        except ModuleNotFoundError:
            raise ModuleNotFoundError("""
            Please installing the package via 'pip install numpy onnxruntime'.
            """)
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
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

    def _load_embeddings(self):
        """Loads embeddings matrix and vocabulary list."""
        input_matrix = self.np.load(os.path.join(self.model_dir, "embeddings.npy"))
        words = []
        vocab_path = os.path.join(self.model_dir, "vocabulary.txt")
        with open(vocab_path, "r", encoding='utf-8') as f:
            for line in f.readlines():
                words.append(line.rstrip())
        return words, input_matrix

    def _load_suggestion_words(self, words_list):
        """Loads the list of words used for suggestions."""
        words = self.np.array(words_list)
        return words

    def _load_onnx_session(self, onnx_path):
        """Loads the ONNX inference session."""
        # Note: Using providers=["CPUExecutionProvider"] for platform independence
        import onnxruntime as rt
        sess = rt.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
        return sess

    # --- Helper Methods for Encoding ---

    def _get_hash(self, subword):
        """Computes the FastText-like hash for a subword."""
        h = 2166136261  # FNV-1a basis
        for c in subword:
            c_ord = ord(c) % 2**8
            h = (h ^ c_ord) % 2**32
            h = (h * 16777619) % 2**32  # FNV-1a prime
        return h % self.bucket + self.nb_words

    def _get_subwords(self, word):
        """Extracts subwords and their corresponding indices for a given word."""
        _word = "<" + word + ">"
        _subwords = []
        _subword_ids = []

        # 1. Check for the word in vocabulary (full word is the first subword)
        if word in self.vocabulary:
            _subwords.append(word)
            _subword_ids.append(self.vocabulary.index(word))
            if word == "</s>":
                return _subwords, self.np.array(_subword_ids)

        # 2. Extract n-grams (subwords) and get their hash indices
        for ngram_start in range(0, len(_word)):
            for ngram_length in range(self.minn, self.maxn + 1):
                if ngram_start + ngram_length <= len(_word):
                    _candidate_subword = _word[ngram_start:ngram_start + ngram_length]
                    # Only append if not already included (e.g., as the full word)
                    if _candidate_subword not in _subwords: 
                        _subwords.append(_candidate_subword)
                        _subword_ids.append(self._get_hash(_candidate_subword))

        return _subwords, self.np.array(_subword_ids)

    def get_word_vector(self, word):
        """Computes the normalized vector for a single word."""
        # subword_ids[1] contains the array of indices for the word and its subwords
        subword_ids = self._get_subwords(word)[1]
        
        # Check if the array of subword indices is empty
        if subword_ids.size == 0:
            # Return a 300-dimensional zero vector if no word/subword is found.
            return self.np.zeros(self.embedding_dim)

        # Compute the mean of the embeddings for all subword indices
        vector = self.np.mean([self.embeddings[s] for s in subword_ids], axis=0)
        
        # Normalize the vector
        norm = self.np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
            
        return vector

    def _tokenize(self, sentence):
        """Tokenizes a sentence based on whitespace."""
        tokens = []
        word = ""
        for c in sentence:
            if c in [' ', '\n', '\r', '\t', '\v', '\f', '\0']:
                if word:
                    tokens.append(word)
                    word = ""
                if c == '\n':
                    tokens.append("</s>")
            else:
                word += c
        if word:
            tokens.append(word)
        return tokens

    def get_sentence_vector(self, line):
        """Computes the mean vector for a sentence."""
        tokens = self._tokenize(line)
        vectors = []
        for t in tokens:
            # get_word_vector already handles normalization, so no need to do it again here
            vec = self.get_word_vector(t)
            vectors.append(vec)
            
        # If the sentence was empty and resulted in no vectors, return a zero vector
        if not vectors:
            return self.np.zeros(self.embedding_dim)

        return self.np.mean(vectors, axis=0)

    # --- Nearest Neighbor Method ---

    def get_word_suggestion(self, list_word):
        """
        Queries the ONNX model to find the nearest neighbor word(s) 
        for the given word or list of words.

        Args:
            list_word (str or list of str): A single word or a list of words 
                                            to get suggestions for.

        Returns:
            str or list of str: The nearest neighbor word(s) from the 
                                pre-loaded suggestion list.
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
        word_input_vecs = [self.get_sentence_vector(' '.join(list(word))) for word in input_words]

        # Convert to numpy array for ONNX input (ensure float32)
        input_data = self.np.array(word_input_vecs, dtype=self.np.float32)

        # Run ONNX inference
        indices = self.nn_session.run(None, {"X": input_data})[0]
        
        # Look up suggestions
        suggestions = [self.words_for_suggestion[i].tolist() for i in indices]
        
        return suggestions[0] if return_single else suggestions


class Words_Spelling_Correction(FastTextEncoder):
    def __init__(self):
        self.model_name = "pythainlp/word-spelling-correction-char2vec"
        self.model_path = get_hf_hub(self.model_name)
        self.model_onnx = get_hf_hub(self.model_name, "nearest_neighbors.onnx")
        with open(get_hf_hub(self.model_name, "list_word-spelling-correction-char2vec.txt")) as f:
            self.list_word = [i.strip() for i in f.readlines()]
        super().__init__(self.model_path, self.model_onnx, self.list_word)


_WSC = None


def get_words_spell_suggestion(list_words: Union[str, List[str]]) -> Union[List[str], List[List[str]]]:
    """
    Get words spell suggestion

    The function is designed to retrieve spelling suggestions \
        for one or more input Thai words.

    Requirements: numpy and onnxruntime (Install before use this function)

    :param Union[str, List[str]] list_word: list words or a word.
    :return: List words spell suggestion (max 5 items per word)
    :rtype: Union[List[str], List[List[str]]]

    :Example:
    ::

        from pythainlp.spell import get_words_spell_suggestion

        print(get_words_spell_suggestion("คมดี"))
        # output: ['คนดีผีคุ้ม', 'มีดคอม้า', 'คดี', 'มีดสองคม', 'มูลคดี']

        print(get_words_spell_suggestion(["คมดี","กระเพาะ"]))
        # output: [['คนดีผีคุ้ม', 'มีดคอม้า', 'คดี', 'มีดสองคม', 'มูลคดี'],
        # ['กระเพาะ', 'กระพา', 'กะเพรา', 'กระเพาะปลา', 'พระประธาน']]
    """
    global _WSC
    if _WSC==None:
        _WSC = Words_Spelling_Correction()
    return _WSC.get_word_suggestion(list_words)
