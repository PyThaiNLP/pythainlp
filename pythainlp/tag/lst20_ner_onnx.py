# -*- coding: utf-8 -*-
from typing import List
from pythainlp.tag.wangchanberta_onnx import WngchanBerta_ONNX


class LST20_NER_ONNX(WngchanBerta_ONNX):
    def __init__(self, providers: List[str] = ['CPUExecutionProvider']) -> None:
        print("""
        LST20 corpus are free for research and open source only.\n
        If you want to use in Commercial use, please contract NECTEC.\n
        https://www.facebook.com/dancearmy/posts/10157641945708284
        """)
        WngchanBerta_ONNX.__init__(
            self,
            model_name="onnx_lst20ner",
            model_version="1.0",
            file_onnx="lst20-ner-model.onnx",
            providers=providers
        )

    def clean_output(self, list_text):
        new_list = []
        if list_text[0][0] == "▁":
            list_text = list_text[1:]
        for i, j in list_text:
            if i.startswith("▁") and i != '▁':
                i = i.replace("▁", "", 1)
            elif i == '▁':
                i = " "
            new_list.append((i, j))
        return new_list

    def _config(self, list_ner):
        _n = []
        for i, j in list_ner:
            _n.append((i, j.replace('E_', 'I_').replace('_', '-')))
        return _n
