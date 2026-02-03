# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Any, Optional

from thai_nner import NNER

from pythainlp.corpus import get_corpus_path


class Thai_NNER:
    def __init__(
        self, path_model: Optional[str] = None
    ) -> None:
        if path_model is None:
            path_model = get_corpus_path("thai_nner", "1.0")
        self.model = NNER(path_model=path_model)

    def tag(self, text: str) -> tuple[list[str], list[dict[str, Any]]]:
        return self.model.get_tag(text)  # type: ignore[no-any-return]
