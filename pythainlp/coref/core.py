# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Any, Optional

_MODEL: Optional[Any] = None


def coreference_resolution(
    texts: Union[str, list[str]],
    model_name: str = "han-coref-v1.0",
    device: str = "cpu",
) -> list[dict]:
    """Coreference Resolution

    :param Union[str, list[str]] texts: list of texts to apply coreference resolution to
    :param str model_name: coreference resolution model
    :param str device: device for running coreference resolution model on\
        ("cpu", "cuda", and others)
    :return: List of texts with coreference resolution
    :rtype: list[dict]

    :Options for model_name:
        * *han-coref-v1.0* - (default) Han-Coref: Thai coreference resolution\
            by PyThaiNLP v1.0

    :Example:
    ::

        from pythainlp.coref import coreference_resolution

        print(
            coreference_resolution(
                ["Bill Gates ได้รับวัคซีน COVID-19 เข็มแรกแล้ว ระบุ ผมรู้สึกสบายมาก"]
            )
        )
        # output:
        # [
        # {'text': 'Bill Gates ได้รับวัคซีน COVID-19 เข็มแรกแล้ว ระบุ ผมรู้สึกสบายมาก',
        # 'clusters_string': [['Bill Gates', 'ผม']],
        # 'clusters': [[(0, 10), (50, 52)]]}
        # ]
    """
    global _MODEL
    if isinstance(texts, str):
        texts = [texts]

    if _MODEL is None and model_name == "han-coref-v1.0":
        from pythainlp.coref.han_coref import HanCoref

        _MODEL = HanCoref(device=device)

    if _MODEL:
        return _MODEL.predict(texts)

    return [
        {"text": text, "clusters_string": [], "clusters": []} for text in texts
    ]
