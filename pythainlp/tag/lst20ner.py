# -*- coding: utf-8 -*-
from typing import List
import sentencepiece as spm
import numpy as np
from onnxruntime import (
    InferenceSession, SessionOptions, GraphOptimizationLevel
)

class lst20ner_onnx:
    def __init__(self, providers: List[str] = ['CPUExecutionProvider']) -> None:
        self.options = SessionOptions()
        self.options.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = InferenceSession(
            "onnx/model.onnx", sess_options=self.options, providers=providers
        )
        self.session.disable_fallback()
        self.outputs_name = self.session.get_outputs()[0].name
        self.sp = spm.SentencePieceProcessor(model_file='cat-model/sentencepiece.bpe.model')
    
    def build_tokenizer(self, sent):
        _t = [5]+[i+4 for i in self.sp.encode(sent)]+[6]
        model_inputs = {}
        model_inputs["input_ids"]=np.array([_t])
        model_inputs["attention_mask"]=np.array([[1]*len(_t)])
        return model_inputs

    def postprocess(self, logits_data):
        logits_t = logits_data[0]
        maxes = np.max(logits_t, axis=-1, keepdims=True)
        shifted_exp = np.exp(logits_t - maxes)
        scores = shifted_exp / shifted_exp.sum(axis=-1, keepdims=True)
        return scores
    
    def totag(self, post,sent):
        tag= []
        _s=self.sp.EncodeAsPieces(sent)
        for i in range(len(_s)):
            tag.append(
                (
                    _s[i],
                    self.id2tag[str(list(post[i+1]).index(max(list(post[i+1]))))]
                )
            )
        return tag
    def get_ner(self, text: str):
        _s=self.build_tokenizer(text)
        logits = self.session.run(output_names=[self.outputs_name], input_feed=_s)[0]
        return self.totag(self.postprocess(logits),text)