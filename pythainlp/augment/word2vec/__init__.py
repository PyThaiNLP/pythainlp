# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Word2Vec"""

__all__: list[str] = ["Word2VecAug", "Thai2fitAug", "LTW2VAug"]

from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.augment.word2vec.ltw2v import LTW2VAug
from pythainlp.augment.word2vec.thai2fit import Thai2fitAug
