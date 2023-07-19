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
from typing import List, Union


class EntityLinker:
    def __init__(self, model_name:str="bela", device:str="cuda", tag:str="wikidata"):
        """
        EntityLinker

        :param str model_name: model name (bela)
        :param str device: device for running model
        :param str tag: Entity linking tag (wikidata)

        You can read about bela model at `https://github.com/PyThaiNLP/MultiEL \
        <https://github.com/PyThaiNLP/MultiEL>`_.
        """
        self.model_name = model_name
        self.device = device
        self.tag = tag
        if self.model_name not in ["bela"]:
            raise NotImplementedError(f"EntityLinker doesn't support {model_name} model.")
        if self.tag not in ["wikidata"]:
            raise NotImplementedError(f"EntityLinker doesn't support {tag} tag.")
        from pythainlp.el._multiel import MultiEL
        self.model = MultiEL(model_name=self.model_name, device=self.device)
    def get_el(self, list_text:Union[List[str], str])->Union[List[dict], str]:
        """
        Get Entity Linking from Thai Text
        
        :param str Union[List[str], str]: list thai text or text
        :return: list of entity linking
        :rtype: Union[List[dict], str]
        
        :Example:
        ::

                from pythainlp.el import EntityLinker
                
                el = EntityLinker(device="cuda")
                print(el.get_el("จ๊อบเคยเป็นซีอีโอบริษัทแอปเปิล"))
                # output: [{'offsets': [11, 23],
                # 'lengths': [6, 7],
                # 'entities': ['Q484876', 'Q312'],
                # 'md_scores': [0.30301809310913086, 0.6399497389793396],
                # 'el_scores': [0.7142490744590759, 0.8657019734382629]}]
        """
        return self.model.process_batch(list_text)
