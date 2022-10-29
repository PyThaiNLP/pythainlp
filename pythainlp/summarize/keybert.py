# -*- coding: utf-8 -*-
"""
Minimal re-implementation of KeyBERT.

KeyBERT is a minimal and easy-to-use keyword extraction technique 
that leverages BERT embeddings to create keywords and keyphrases 
that are most similar to a document.

https://github.com/MaartenGr/KeyBERT
"""
from typing import List, Optional, Iterable, Tuple, Union
from collections import Counter

import numpy as np
from transformers import AutoTokenizer, pipeline

from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import word_tokenize


class KeyBERT:
    def __init__(self, model_name: str="airesearch/wangchanberta-base-att-spm-uncased"):
        tokenizer = AutoTokenizer.from_pretrained(model_name, revision="main")
        self.ft_pipeline = pipeline("feature-extraction", tokenizer=tokenizer, model=model_name, revision="main")

    def extract_keywords(
            self, 
            doc: str, 
            keyphrase_ngram_range: Tuple[int, int]=(1, 2), 
            max_keywords: int=5,            
            min_df: int=1, 
            tokenizer: str='newmm',
            stop_words: Optional[Iterable[str]]=None
        ) -> List[Tuple[str, float]]:
        """
        Extract Thai keywords and/or keyphrases
        """
        try:
            doc = doc.strip()
        except AttributeError:
            raise AttributeError(
                f"Unable to process data of type {type(doc)}. "
                f"Please provide input of string type."
            )
        
        if not doc:
            return []
        
        # generate all list of keyword / keyphrases
        stop_words_ = stop_words if stop_words else thai_stopwords()
        kw_candidates = _generate_ngrams(doc, keyphrase_ngram_range, min_df, tokenizer, stop_words_)

        # create document and word vectors
        doc_vector = self.embed(doc)
        kw_vectors = self.embed(kw_candidates)

        # rank keywords
        keywords = _rank_keywords(doc_vector, kw_vectors, kw_candidates, max_keywords)

        return keywords

    def embed(self, docs: Union[str, List[str]]) -> np.ndarray:
        embs = self.ft_pipeline(docs)
        if isinstance(docs, str) or len(docs) == 1:
            # embed doc. return shape = [1, hidden_size]
            emb_mean = np.array(embs).mean(axis=1)
        else:
            # mean of embedding of each word
            # return shape = [len(docs), hidden_size]
            emb_mean = np.stack([np.array(emb[0]).mean(axis=0) for emb in embs])
        
        return emb_mean


def _generate_ngrams(
        doc: str, 
        keyphrase_ngram_range: Tuple[int, int],
        min_df: int, 
        tokenizer_engine: str,
        stop_words: Iterable[str]
    ) -> List[str]:
    assert keyphrase_ngram_range[0] >= 1, (
        f"`keyphrase_ngram_range` must start from 1. "
        f"current value={keyphrase_ngram_range}."
    )
    
    assert keyphrase_ngram_range[0] <= keyphrase_ngram_range[1], (
        f"The value first argument of `keyphrase_ngram_range` must not exceed the second. "
        f"current value={keyphrase_ngram_range}."
    )
    def _join_ngram(ngrams: List[Tuple[str, str]]) -> List[str]:
        ngrams_joined = []
        for ng in ngrams:
            joined = "".join(ng)
            if joined.strip() == joined:
                # ngram must not start or end with whitespace as this may cause duplication.
                ngrams_joined.append(joined)
        return ngrams_joined

    words = word_tokenize(doc, engine=tokenizer_engine)
    all_grams = []
    ngram_range = (keyphrase_ngram_range[0], keyphrase_ngram_range[1] + 1)
    for n in range(*ngram_range):
        if n == 1:
            # filter out space
            ngrams = [word for word in words if word.strip()]
        else:
            ngrams_tuple = zip(*[words[i:] for i in range(n)])
            ngrams = _join_ngram(ngrams_tuple)

        ngrams_cnt = Counter(ngrams)
        ngrams = [word for word, freq in ngrams_cnt.items() if (freq >= min_df) and (word not in stop_words)]
        all_grams.extend(ngrams)
    
    return all_grams


def _rank_keywords(doc_vector: np.ndarray, word_vectors: np.ndarray, keywords: List[str], max_keywords: int)->List[Tuple[str, float]]:
    def l2_norm(v: np.ndarray) -> np.ndarray:
        vec_size = v.shape[1]
        result = np.divide(v, np.linalg.norm(v, axis=1).reshape(-1, 1).repeat(vec_size, axis=1))
        assert np.isclose(np.linalg.norm(result, axis=1), 1).all(), "Cannot normalize a vector to unit vector."
        return result
    
    def cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return (np.matmul(a, b.T).T).sum(axis=1)

    doc_vector = l2_norm(doc_vector)
    word_vectors = l2_norm(word_vectors)
    cosine_sims = cosine_sim(doc_vector, word_vectors)
    ranking_desc = np.argsort(-cosine_sims)

    final_ranks = [(keywords[r], cosine_sims[r]) for r in ranking_desc[:max_keywords]]
    return final_ranks    
