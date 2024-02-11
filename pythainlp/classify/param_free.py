# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import gzip
from typing import List, Tuple
import numpy as np


class GzipModel:
    """
    This class is a re-implementation of
    “Low-Resource” Text Classification: A Parameter-Free Classification Method with Compressors
    (Jiang et al., Findings 2023)

    :param list training_data: list [(text_sample,label)]
    """

    def __init__(self, training_data: List[Tuple[str, str]]):
        self.training_data = np.array(training_data)
        self.Cx2_list = self.train()

    def train(self):
        Cx2_list = []
        for i in range(len(self.training_data)):
            Cx2_list.append(
                len(gzip.compress(self.training_data[i][0].encode("utf-8")))
            )
        return Cx2_list

    def predict(self, x1: str, k: int = 1) -> str:
        """
        :param str x1: the text that we want to predict label for.
        :param str k: k
        :return: label
        :rtype: str

        :Example:
        ::

                from pythainlp.classify import GzipModel

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
