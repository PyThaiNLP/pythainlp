# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union, cast

if TYPE_CHECKING:
    from multiel import BELA


class MultiEL:
    model_name: str
    device: str
    _bela_run: BELA

    def __init__(self, model_name: str = "bela", device: str = "cuda") -> None:
        self.model_name: str = model_name
        self.device: str = device
        self.load_model()

    def load_model(self) -> None:
        try:
            from multiel import BELA
        except ImportError as exc:
            raise ImportError(
                "Can't import multiel package, you can install by pip install multiel."
            ) from exc
        self._bela_run: "BELA" = BELA(device=self.device)

    def process_batch(
        self, list_text: Union[list[str], str]
    ) -> Union[list[dict[str, Any]], str]:
        if isinstance(list_text, str):
            list_text = [list_text]
        return cast(
            Union[list[dict[str, Any]], str],
            self._bela_run.process_batch(list_text),
        )
