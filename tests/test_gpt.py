# -*- coding: utf-8 -*-

import unittest
from pythainlp.gpt.gpt_neo import FewShot


class TestGPTackage(unittest.TestCase):
    def test_gpt_neo_fewshot(self):
        _model = FewShot('./')
        self.assertIsNotNone(_model)
        _data = [
            'txt: คนดี pos: +',
            'txt: คนเลว pos: -'
        ]
        self.assertIsNone(_model.train(_data, './log', num_train_epochs=1))
        self.assertIsNotNone(_model.gen('txt: คนชั่ว pos:'))
        del _model
        self.assertIsNotNone(FewShot('./'))
