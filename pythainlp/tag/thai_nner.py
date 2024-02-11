# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List, Tuple
from thai_nner import NNER
from pythainlp.corpus import get_corpus_path


class Thai_NNER:
    def __init__(self, path_model=get_corpus_path("thai_nner", "1.0")) -> None:
        self.model = NNER(path_model=path_model)

    def tag(self, text) -> Tuple[List[str], List[dict]]:
        return self.model.get_tag(text)
