# -*- coding: utf-8 -*-
from typing import List
from pythainlp.tag.wangchanberta_onnx import WngchanBerta_ONNX


class LST20_ONNX(WngchanBerta_ONNX):
    def __init__(self, providers: List[str] = ['CPUExecutionProvider']) -> None:
        WngchanBerta_ONNX.__init__(
            self,
            model_name="onnx_lst20ner",
            model_version="1.0",
            file_onnx="lst20-ner-model.onnx",
            providers=providers
        )
