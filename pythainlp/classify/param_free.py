# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import gzip
import json
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from numpy.typing import NDArray


class GzipModel:
    """This class is a re-implementation of
    “Low-Resource” Text Classification: A Parameter-Free Classification Method
    with Compressors (Jiang et al., Findings 2023)

    :param Optional[list] training_data: list [(text_sample,label)].
        Default is None.
    :param str model_path: Path for loading model (if you saved the model).
        Default is empty string.
    """

    cx2_list: list[int]
    training_data: "NDArray[Any]"

    def __init__(
        self,
        training_data: Optional[list[tuple[str, str]]] = None,
        model_path: str = "",
    ) -> None:
        import numpy as np

        if model_path:
            self.load(model_path)
        else:
            self.training_data = np.array(training_data)
            self.cx2_list = self.train()

    def train(self) -> list[int]:
        temp_list = []
        for i in range(len(self.training_data)):
            temp_list.append(
                len(gzip.compress(self.training_data[i][0].encode("utf-8")))
            )
        return temp_list

    def predict(self, x1: str, k: int = 1) -> str:
        """Predict the label for the given text.

        :param str x1: the text that we want to predict label for
        :param int k: number of nearest neighbors to consider (default: 1)
        :return: predicted label
        :rtype: str

        :Example:

            >>>     from pythainlp.classify import GzipModel  # doctest: +SKIP

            >>>     training_data = [  # doctest: +SKIP
            ...         ("รายละเอียดตามนี้เลยค่าา ^^", "Neutral"),
            ...         ("กลัวพวกมึงหาย อดกินบาบิก้อน", "Neutral"),
            ...         ("บริการแย่มากก เป็นหมอได้ไง😤", "Negative"),
            ...         ("ขับรถแย่มาก", "Negative"),
            ...         ("ดีนะครับ", "Positive"),
            ...         ("ลองแล้วรสนี้อร่อย... ชอบๆ", "Positive"),
            ...         ("ฉันรู้สึกโกรธ เวลามือถือแบตหมด", "Negative"),
            ...         ("เธอภูมิใจที่ได้ทำสิ่งดี ๆ และดีใจกับเด็ก ๆ", "Positive"),
            ...         ("นี่เป็นบทความหนึ่ง", "Neutral"),
            ...     ]
            >>>     model = GzipModel(training_data)  # doctest: +SKIP
            >>>     print(model.predict("ฉันดีใจ", k=1))  # doctest: +SKIP
                Positive
        """
        import numpy as np

        cx1 = len(gzip.compress(x1.encode("utf-8")))
        disance_from_x1 = []
        for i in range(len(self.cx2_list)):
            x2 = self.training_data[i][0]
            cx2 = self.cx2_list[i]
            x1x2 = "".join([x1, x2])
            cx1x2 = len(gzip.compress(x1x2.encode("utf-8")))
            # normalized compression distance
            ncd = (cx1x2 - min(cx1, cx2)) / max(cx1, cx2)
            disance_from_x1.append(ncd)

        sorted_idx = np.argsort(np.array(disance_from_x1))
        top_k_class = self.training_data[sorted_idx[:k], 1]
        _, counts = np.unique(top_k_class, return_counts=True)
        predict_class = str(top_k_class[counts.argmax()])

        return predict_class

    def save(self, path: str) -> None:
        """Save model to file.

        :param str path: path to save model
        """
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "training_data": self.training_data.tolist(),
                    "cx2_list": self.cx2_list,
                },
                f,
                ensure_ascii=False,
            )

    def load(self, path: str) -> None:
        """Load model from file.

        :param str path: path to load model from
        """
        import numpy as np

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.cx2_list = data["cx2_list"]
            self.training_data = np.array(data["training_data"])
