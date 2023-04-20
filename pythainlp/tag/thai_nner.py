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
from typing import List, Tuple
from thai_nner import NNER
from pythainlp.corpus import get_corpus_path


class Thai_NNER:
    def __init__(self, path_model=get_corpus_path("thai_nner", "1.0")) -> None:
        self.model = NNER(path_model=path_model)

    def tag(self, text) -> Tuple[List[str], List[dict]]:
        return self.model.get_tag(text)
