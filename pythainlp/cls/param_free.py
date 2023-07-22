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

import gzip
import numpy as np
from typing import Dict, List, Tuple, Union


class GzipModel:
    """
    This class is a reimplemenatation of “Low-Resource” Text Classification: A Parameter-Free Classification Method with Compressors (Jiang et al., Findings 2023)

    :param list training_data: list [(text_sample,label)]
    """

    def __init__(self, training_data: List[Tuple[str, str]]):
        self.training_data = np.array(training_data)
        self.Cx2_list = self.train()

    def train(self):
        Cx2_list = list()
        for i in range(len(self.training_data)):
            Cx2_list.append(
                len(gzip.compress(self.training_data[i][0].encode("utf-8")))
            )
        return Cx2_list

    def predict(self, x1: str, k: int = 1) -> str:
        """
        :param str x1: the text that want to predict label.
        :param str k: k
        :return: label
        :rtype: str

        :Example:
        ::

                from pythainlp.cls import GzipModel

                training_data =  [
                    ("รายละเอียดตามนี้เลยค่าา ^^", "Neutral"),
                    ("กลัวพวกมึงหาย อดกินบาบิก้อน", "Neutral"),
                    ("บริการแย่มากก เป็นหมอได้ไง😤", "Negative"),
                    ("ขับรถแย่มาก", "Negative"),
                    ("ดีนะครับ", "Positive"),
                    ("ลองแล้วรสนี้อร่อย... ชอบๆ", "Positive"),
                    ("ฉันรู้สึกโกรธ เวลามือถือแบตหมด", "Negative"),
                    ("เธอภูมิใจที่ได้ทำสิ่งดี ๆ และดีใจกับเด็ก ๆ", "Positive"),
                    ("นี่เป็นบทความหนึ่ง", "Neutral")
                ]
                model = GzipModel(training_data)
                print(model.predict("ฉันดีใจ", k=1))
                # output: Positive
        """
        Cx1 = len(gzip.compress(x1.encode("utf-8")))
        disance_from_x1 = []
        for i in range(len(self.Cx2_list)):
            x2 = self.training_data[i][0]
            Cx2 = self.Cx2_list[i]
            x1x2 = "".join([x1, x2])
            Cx1x2 = len(gzip.compress(x1x2.encode("utf-8")))
            # normalized compression distance
            ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)
            disance_from_x1.append(ncd)
        sorted_idx = np.argsort(np.array(disance_from_x1))
        top_k_class = self.training_data[sorted_idx[:k], 1]
        _, counts = np.unique(top_k_class, return_counts=True)
        predict_class = top_k_class[counts.argmax()]
        return predict_class
