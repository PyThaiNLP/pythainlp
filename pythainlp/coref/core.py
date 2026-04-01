# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Any, Union, cast

from pythainlp.coref._fastcoref import CorefResult

_MODEL_CACHE: dict[tuple[str, str], Any] = {}


def coreference_resolution(
    texts: Union[str, list[str]],
    model_name: str = "han-coref-v1.0",
    device: str = "cpu",
) -> list[CorefResult]:
    """Coreference Resolution

    :param Union[str, list[str]] texts: list of texts to apply coreference resolution to
    :param str model_name: coreference resolution model
    :param str device: device for running coreference resolution model on\
        ("cpu", "cuda", and others)
    :return: List of texts with coreference resolution
    :rtype: list[CorefResult]

    :Options for model_name:
        * *han-coref-v1.0* - (default) Han-Coref: Thai coreference resolution\
            by PyThaiNLP v1.0

    :Example:

        >>> from pythainlp.coref import coreference_resolution  # doctest: +SKIP

        >>> print(  # doctest: +SKIP
        ...     coreference_resolution(
        ...         ["Bill Gates ได้รับวัคซีน COVID-19 เข็มแรกแล้ว ระบุ ผมรู้สึกสบายมาก"]
        ...     )
        ... )
        [
        {'text': 'Bill Gates ได้รับวัคซีน COVID-19 เข็มแรกแล้ว ระบุ ผมรู้สึกสบายมาก',
        'clusters_string': [['Bill Gates', 'ผม']],
        'clusters': [[(0, 10), (50, 52)]]}
        ]
    """
    if isinstance(texts, str):
        texts = [texts]

    model_key = (model_name, device)
    if model_key not in _MODEL_CACHE and model_name == "han-coref-v1.0":
        from pythainlp.coref.han_coref import HanCoref

        _MODEL_CACHE[model_key] = HanCoref(device=device)

    model = _MODEL_CACHE.get(model_key)
    if model is not None:
        return cast(list[CorefResult], model.predict(texts))

    return [
        CorefResult(text=text, clusters_string=[], clusters=[])
        for text in texts
    ]
