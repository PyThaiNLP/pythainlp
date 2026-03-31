# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Any, Union


class EntityLinker:
    def __init__(
        self,
        model_name: str = "bela",
        device: str = "cuda",
        tag: str = "wikidata",
    ) -> None:
        """EntityLinker

        :param str model_name: model name (bela)
        :param str device: device for running model on
        :param str tag: Entity linking tag (wikidata)

        You can read about bela model at `https://github.com/PyThaiNLP/MultiEL \
        <https://github.com/PyThaiNLP/MultiEL>`_.
        """
        self.model_name: str = model_name
        self.device: str = device
        self.tag: str = tag
        if self.model_name not in ["bela"]:
            raise NotImplementedError(
                f"EntityLinker doesn't support {model_name} model."
            )
        if self.tag not in ["wikidata"]:
            raise NotImplementedError(
                f"EntityLinker doesn't support {tag} tag."
            )
        from pythainlp.el._multiel import MultiEL

        self.model: MultiEL = MultiEL(
            model_name=self.model_name, device=self.device
        )

    def get_el(
        self, list_text: Union[list[str], str]
    ) -> Union[list[dict[str, Any]], str]:
        """Get Entity Linking from Thai Text

        :param Union[list[str], str] list_text: list of Thai text or text
        :return: list of entity linking
        :rtype: Union[list[dict[str, Any]], str]

        :Example:

            >>>     from pythainlp.el import EntityLinker  # doctest: +SKIP

            >>>     el = EntityLinker(device="cuda")  # doctest: +SKIP
            >>>     print(el.get_el("จ๊อบเคยเป็นซีอีโอบริษัทแอปเปิล"))  # doctest: +SKIP
                [{'offsets': [11, 23],
                'lengths': [6, 7],
                'entities': ['Q484876', 'Q312'],
                'md_scores': [0.30301809310913086, 0.6399497389793396],
                'el_scores': [0.7142490744590759, 0.8657019734382629]}]
        """
        return self.model.process_batch(list_text)
