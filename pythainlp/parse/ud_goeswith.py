# -*- coding: utf-8 -*-
"""
UDgoeswith

Author: Prof. Koichi Yasuoka

This tagger is provided under the terms of the apache-2.0 License.

The source: https://huggingface.co/KoichiYasuoka/deberta-base-thai-ud-goeswith

GitHub: https://github.com/KoichiYasuoka
"""
from typing import List, Union

import numpy as np
import torch
import ufal.chu_liu_edmonds
from transformers import AutoModelForTokenClassification, AutoTokenizer


class Parse:
    def __init__(
        self, model: str = "KoichiYasuoka/deberta-base-thai-ud-goeswith"
    ) -> None:
        if model is None:
            model = "KoichiYasuoka/deberta-base-thai-ud-goeswith"
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForTokenClassification.from_pretrained(model)

    def __call__(
        self, text: str, tag: str = "str"
    ) -> Union[List[List[str]], str]:
        w = self.tokenizer(text, return_offsets_mapping=True)
        v = w["input_ids"]
        x = [
            v[0:i] + [self.tokenizer.mask_token_id] + v[i + 1 :] + [j]
            for i, j in enumerate(v[1:-1], 1)
        ]
        with torch.no_grad():
            e = self.model(input_ids=torch.tensor(x)).logits.numpy()[
                :, 1:-2, :
            ]
        r = [
            1 if i == 0 else -1 if j.endswith("|root") else 0
            for i, j in sorted(self.model.config.id2label.items())
        ]
        e += np.where(np.add.outer(np.identity(e.shape[0]), r) == 0, 0, np.nan)
        g = self.model.config.label2id["X|_|goeswith"]
        r = np.tri(e.shape[0])
        for i in range(e.shape[0]):
            for j in range(i + 2, e.shape[1]):
                r[i, j] = r[i, j - 1] if np.nanargmax(e[i, j - 1]) == g else 1
        e[:, :, g] += np.where(r == 0, 0, np.nan)
        m = np.full((e.shape[0] + 1, e.shape[1] + 1), np.nan)
        m[1:, 1:] = np.nanmax(e, axis=2).transpose()
        p = np.zeros(m.shape)
        p[1:, 1:] = np.nanargmax(e, axis=2).transpose()
        for i in range(1, m.shape[0]):
            m[i, 0], m[i, i], p[i, 0] = m[i, i], np.nan, p[i, i]
        h = ufal.chu_liu_edmonds.chu_liu_edmonds(m)[0]
        if [0 for i in h if i == 0] != [0]:
            m[:, 0] += np.where(
                m[:, 0]
                == np.nanmax(m[[i for i, j in enumerate(h) if j == 0], 0]),
                0,
                np.nan,
            )
            m[[i for i, j in enumerate(h) if j == 0]] += [
                0 if i == 0 or j == 0 else np.nan for i, j in enumerate(h)
            ]
            h = ufal.chu_liu_edmonds.chu_liu_edmonds(m)[0]
        u = ""
        v = [(s, e) for s, e in w["offset_mapping"] if s < e]
        if tag == "list":
            _tag_data = []
            for i, (s, e) in enumerate(v, 1):
                q = self.model.config.id2label[p[i, h[i]]].split("|")
                _tag_data.append(
                    [
                        str(i),
                        text[s:e],
                        "_",
                        q[0],
                        "_",
                        "|".join(q[1:-1]),
                        str(h[i]),
                        q[-1],
                        "_",
                        "_" if i < len(v) and e < v[i][0] else "SpaceAfter=No",
                    ]
                )
            return _tag_data
        else:
            for i, (s, e) in enumerate(v, 1):
                q = self.model.config.id2label[p[i, h[i]]].split("|")
                u += (
                    "\t".join(
                        [
                            str(i),
                            text[s:e],
                            "_",
                            q[0],
                            "_",
                            "|".join(q[1:-1]),
                            str(h[i]),
                            q[-1],
                            "_",
                            "_"
                            if i < len(v) and e < v[i][0]
                            else "SpaceAfter=No",
                        ]
                    )
                    + "\n"
                )
            return u + "\n"
