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


class MultiEL:
    def __init__(self, model_name="bela", device="cuda"):
        self.model_name = model_name
        self.device = device
        self.load_model()
    def load_model(self):
        try:
            from multiel import BELA
        except ImportError:
            raise ImportError(
                "Can't import multiel package, you can install by pip install multiel."
            )
        self._bela_run = BELA(device=self.device)
    def process_batch(self, list_text):
        if isinstance(list_text, str):
            list_text = [list_text]
        return self._bela_run.process_batch(list_text)