# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0


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
