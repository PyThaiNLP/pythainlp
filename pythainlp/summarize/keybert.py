# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Minimal re-implementation of KeyBERT.

KeyBERT is a minimal and easy-to-use keyword extraction technique
that leverages BERT embeddings to create keywords and keyphrases
that are most similar to a document.

https://github.com/MaartenGr/KeyBERT
"""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Optional, Union, cast

from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import word_tokenize

if TYPE_CHECKING:
    from collections.abc import Iterable

    import numpy as np
    from numpy.typing import NDArray
    from transformers.pipelines.base import Pipeline


class KeyBERT:
    ft_pipeline: "Pipeline"

    def __init__(
        self, model_name: str = "airesearch/wangchanberta-base-att-spm-uncased"
    ) -> None:
        from transformers import pipeline

        self.ft_pipeline: "Pipeline" = pipeline(
            "feature-extraction",
            tokenizer=model_name,
            model=model_name,
            revision="main",
        )

    def extract_keywords(
        self,
        text: str,
        keyphrase_ngram_range: tuple[int, int] = (1, 2),
        max_keywords: int = 5,
        min_df: int = 1,
        tokenizer: str = "newmm",
        return_similarity: bool = False,
        stop_words: Optional[Iterable[str]] = None,
    ) -> Union[list[str], list[tuple[str, float]]]:
        """Extract Thai keywords and/or keyphrases with KeyBERT algorithm.
        See https://github.com/MaartenGr/KeyBERT.

        :param str text: text to be summarized
        :param Tuple[int, int] keyphrase_ngram_range: Number of token units to be defined as keyword.
                                The token unit varies w.r.t. `tokenizer_engine`.
                                For instance, (1, 1) means each token (unigram) can be a keyword (e.g. "เสา", "ไฟฟ้า"),
                                (1, 2) means one and two consecutive tokens (unigram and bigram) can be keywords
                                (e.g. "เสา", "ไฟฟ้า", "เสาไฟฟ้า")  (default: (1, 2))
        :param int max_keywords: Number of maximum keywords to be returned. (default: 5)
        :param int min_df: Minimum frequency required to be a keyword. (default: 1)
        :param str tokenizer: Name of tokenizer engine to use.
                                Refer to options in :func: `pythainlp.tokenize.word_tokenizer() (default: 'newmm')
        :param bool return_similarity: If `True`, return keyword scores. (default: False)
        :param Optional[Iterable[str]] stop_words: A list of stop words (a.k.a words to be ignored).
                                If not specified, :func:`pythainlp.corpus.thai_stopwords` is used. (default: None)

        :return: list of keywords with score

        :Example:

            >>> from pythainlp.summarize.keybert import KeyBERT  # doctest: +SKIP

            >>> text = '''  # doctest: +SKIP
            ...     อาหาร หมายถึง ของแข็งหรือของเหลว
            ...     ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว
            ...     จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย
            ...     ทำให้ร่างกายเจริญเติบโต
            ...     ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย
            ...     ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ
            ...     อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย
            ... '''

            >>> kb = KeyBERT()  # doctest: +SKIP

            >>> keywords = kb.extract_keyword(text)  # doctest: +SKIP

            ['อวัยวะต่างๆ',
            'ซ่อมแซมส่วน',
            'เจริญเติบโต',
            'ควบคุมการเปลี่ยนแปลง',
            'มีพิษ']

            >>> keywords = kb.extract_keyword(  # doctest: +SKIP
            ...     text, max_keywords=10, return_similarity=True
            ... )

            [('อวัยวะต่างๆ', 0.3228477063109462),
            ('ซ่อมแซมส่วน', 0.31320597838000375),
            ('เจริญเติบโต', 0.29115434699705506),
            ('ควบคุมการเปลี่ยนแปลง', 0.2678430841321016),
            ('มีพิษ', 0.24996827960821494),
            ('ทำให้ร่างกาย', 0.23876962942443258),
            ('ร่างกายเจริญเติบโต', 0.23191285218852364),
            ('จะทำให้เกิด', 0.22425422716846247),
            ('มีพิษและ', 0.22162962875299588),
            ('เกิดโทษ', 0.20773497763458507)]

        """
        try:
            text = text.strip()
        except AttributeError as exc:
            raise AttributeError(
                f"Unable to process data of type {type(text)}. "
                f"Please provide input of string type."
            ) from exc

        if not text:
            return []

        # generate all lists of keywords / keyphrases
        stop_words_ = stop_words if stop_words else thai_stopwords()
        kw_candidates = _generate_ngrams(
            text, keyphrase_ngram_range, min_df, tokenizer, stop_words_
        )

        # create document and word vectors
        doc_vector = self.embed(text)
        kw_vectors = self.embed(kw_candidates)

        # rank keywords
        keywords = _rank_keywords(
            doc_vector, kw_vectors, kw_candidates, max_keywords
        )

        if return_similarity:
            return keywords
        else:
            return [kw for kw, _ in keywords]

    def embed(self, docs: Union[str, list[str]]) -> "NDArray[np.float32]":
        """Create embeddings by averaging vectors from the last hidden layer.

        :param Union[str, list[str]] docs: input document or documents
        :return: embeddings as a float32 array with one row per input document
        :rtype: numpy.typing.NDArray[numpy.float32]
        """
        import numpy as np

        embs = self.ft_pipeline(docs)
        if isinstance(docs, str) or len(docs) == 1:
            # embed doc. return shape = [1, hidden_size]
            emb_mean = np.array(embs, dtype=np.float32).mean(
                axis=1, dtype=np.float32
            )
        else:
            # mean of embedding of each word
            # return shape = [len(docs), hidden_size]
            emb_mean = np.stack(
                [np.array(emb[0]).mean(axis=0) for emb in embs]
            ).astype(np.float32)

        return cast("NDArray[np.float32]", emb_mean)


def _generate_ngrams(
    doc: str,
    keyphrase_ngram_range: tuple[int, int],
    min_df: int,
    tokenizer_engine: str,
    stop_words: Iterable[str],
) -> list[str]:
    if keyphrase_ngram_range[0] < 1:
        raise ValueError(
            f"`keyphrase_ngram_range` must start from 1. "
            f"current value={keyphrase_ngram_range}."
        )

    if keyphrase_ngram_range[0] > keyphrase_ngram_range[1]:
        raise ValueError(
            f"The value first argument of `keyphrase_ngram_range` must not exceed the second. "
            f"current value={keyphrase_ngram_range}."
        )

    def _join_ngram(ngrams: list[tuple[str, ...]]) -> list[str]:
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
            ngrams = _join_ngram(list(ngrams_tuple))

        ngrams_cnt = Counter(ngrams)
        ngrams = [
            word
            for word, freq in ngrams_cnt.items()
            if (freq >= min_df) and (word not in stop_words)
        ]
        all_grams.extend(ngrams)

    return all_grams


def _rank_keywords(
    doc_vector: "NDArray[np.float32]",
    word_vectors: "NDArray[np.float32]",
    keywords: list[str],
    max_keywords: int,
) -> list[tuple[str, float]]:
    import numpy as np

    def l2_norm(v: "NDArray[np.float32]") -> "NDArray[np.float32]":
        vec_size = v.shape[1]
        result = np.divide(
            v,
            np.linalg.norm(v, axis=1).reshape(-1, 1).repeat(vec_size, axis=1),
            dtype=np.float32,
        )
        if not np.isclose(np.linalg.norm(result, axis=1), 1).all():
            raise ValueError("Cannot normalize a vector to unit vector.")
        return cast("NDArray[np.float32]", result)

    def cosine_sim(
        a: "NDArray[np.float32]", b: "NDArray[np.float32]"
    ) -> "NDArray[np.float32]":
        # `a` has one row (document embedding), so flatten to get 1-D scores.
        scores = np.matmul(a, b.T).reshape(-1)
        return cast("NDArray[np.float32]", scores.astype(np.float32, copy=False))

    doc_vector = l2_norm(doc_vector)
    word_vectors = l2_norm(word_vectors)
    cosine_sims = cosine_sim(doc_vector, word_vectors)
    ranking_desc = np.argsort(-cosine_sims)

    top_indices = cast("list[int]", ranking_desc[:max_keywords].tolist())
    final_ranks = [
        (keywords[idx], float(cosine_sims[idx])) for idx in top_indices
    ]
    return final_ranks
