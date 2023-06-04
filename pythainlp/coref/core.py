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
from typing import List
model = None


def coreference_resolution(texts:List[str], model_name:str="han-coref-v1.0", device:str="cpu"):
    """
    Coreference Resolution

    :param List[str] texts: list texts to do coreference resolution
    :param str model_name: coreference resolution model
    :param str device: device for running coreference resolution model (cpu, cuda, and other)
    :return: List txets of coreference resolution
    :rtype: List[dict]

    :Options for model_name:
        * *han-coref-v1.0* - (default) Han-Corf: Thai oreference resolution by PyThaiNLP v1.0

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
    global model
    if isinstance(texts, str):
        texts = [texts]
    if model == None and model_name=="han-coref-v1.0":
        from pythainlp.coref.han_coref import HanCoref
        model = HanCoref(device=device)
    return model.predict(texts)