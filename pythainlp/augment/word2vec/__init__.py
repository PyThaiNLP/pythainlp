# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Word2Vec
"""

__all__ = ["Word2VecAug", "Thai2fitAug", "LTW2VAug"]

from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.augment.word2vec.thai2fit import Thai2fitAug
from pythainlp.augment.word2vec.ltw2v import LTW2VAug
