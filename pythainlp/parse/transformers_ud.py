# -*- coding: utf-8 -*-
"""
TransformersUD

Author: Prof. Koichi Yasuoka

This tagger is provided under the terms of the apache-2.0 License.

The source: https://huggingface.co/KoichiYasuoka/deberta-base-thai-ud-head

GitHub: https://github.com/KoichiYasuoka
"""
import os
from typing import List, Union

import numpy
import torch
import ufal.chu_liu_edmonds
from transformers import (
    AutoConfig,
    AutoModelForQuestionAnswering,
    AutoModelForTokenClassification,
    AutoTokenizer,
    TokenClassificationPipeline,
)
from transformers.utils import cached_file


class Parse:
    def __init__(
        self, model: str = "KoichiYasuoka/deberta-base-thai-ud-head"
    ) -> None:
        if model is None:
            model = "KoichiYasuoka/deberta-base-thai-ud-head"
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model)
        x = AutoModelForTokenClassification.from_pretrained
        if os.path.isdir(model):
            d, t = (
                x(os.path.join(model, "deprel")),
                x(os.path.join(model, "tagger")),
            )
        else:
            c = AutoConfig.from_pretrained(
                cached_file(model, "deprel/config.json")
            )
            d = x(cached_file(model, "deprel/pytorch_model.bin"), config=c)
            s = AutoConfig.from_pretrained(
                cached_file(model, "tagger/config.json")
            )
            t = x(cached_file(model, "tagger/pytorch_model.bin"), config=s)
        self.deprel = TokenClassificationPipeline(
            model=d, tokenizer=self.tokenizer, aggregation_strategy="simple"
        )
        self.tagger = TokenClassificationPipeline(
            model=t, tokenizer=self.tokenizer
        )

    def __call__(
        self, text: str, tag: str = "str"
    ) -> Union[List[List[str]], str]:
        w = [
            (t["start"], t["end"], t["entity_group"])
            for t in self.deprel(text)
        ]
        z, n = (
            {t["start"]: t["entity"].split("|") for t in self.tagger(text)},
            len(w),
        )
        r, m = (
            [text[s:e] for s, e, p in w],
            numpy.full((n + 1, n + 1), numpy.nan),
        )
        v, c = self.tokenizer(r, add_special_tokens=False)["input_ids"], []
        for i, t in enumerate(v):
            q = (
                [self.tokenizer.cls_token_id]
                + t
                + [self.tokenizer.sep_token_id]
            )
            c.append(
                [q]
                + v[0:i]
                + [[self.tokenizer.mask_token_id]]
                + v[i + 1 :]
                + [[q[-1]]]
            )
        b = [[len(sum(x[0 : j + 1], [])) for j in range(len(x))] for x in c]
        with torch.no_grad():
            d = self.model(
                input_ids=torch.tensor([sum(x, []) for x in c]),
                token_type_ids=torch.tensor(
                    [[0] * x[0] + [1] * (x[-1] - x[0]) for x in b]
                ),
            )
        s, e = d.start_logits.tolist(), d.end_logits.tolist()
        for i in range(n):
            for j in range(n):
                m[i + 1, 0 if i == j else j + 1] = (
                    s[i][b[i][j]] + e[i][b[i][j + 1] - 1]
                )
        h = ufal.chu_liu_edmonds.chu_liu_edmonds(m)[0]
        if [0 for i in h if i == 0] != [0]:
            i = ([p for s, e, p in w] + ["root"]).index("root")
            j = i + 1 if i < n else numpy.nanargmax(m[:, 0])
            m[0:j, 0] = m[j + 1 :, 0] = numpy.nan
            h = ufal.chu_liu_edmonds.chu_liu_edmonds(m)[0]
        u = ""
        if tag == "list":
            _tag_data = []
            for i, (s, e, p) in enumerate(w, 1):
                p = "root" if h[i] == 0 else "dep" if p == "root" else p
                _tag_data.append(
                    [
                        str(i),
                        r[i - 1],
                        "_",
                        z[s][0][2:],
                        "_",
                        "|".join(z[s][1:]),
                        str(h[i]),
                        p,
                        "_",
                        "_" if i < n and e < w[i][0] else "SpaceAfter=No",
                    ]
                )
            return _tag_data
        for i, (s, e, p) in enumerate(w, 1):
            p = "root" if h[i] == 0 else "dep" if p == "root" else p
            u += (
                "\t".join(
                    [
                        str(i),
                        r[i - 1],
                        "_",
                        z[s][0][2:],
                        "_",
                        "|".join(z[s][1:]),
                        str(h[i]),
                        p,
                        "_",
                        "_" if i < n and e < w[i][0] else "SpaceAfter=No",
                    ]
                )
                + "\n"
            )
        return u + "\n"
