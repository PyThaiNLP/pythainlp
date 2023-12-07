# -*- coding: utf-8 -*-

import pickle
import unittest

import pandas as pd
import torch

# fastai
import fastai
from fastai.text import *
from pythainlp.tokenize import THAI2FIT_TOKENIZER
from pythainlp.ulmfit import (
    THWIKI_LSTM,
    ThaiTokenizer,
    document_vector,
    merge_wgts,
    post_rules_th,
    post_rules_th_sparse,
    pre_rules_th,
    pre_rules_th_sparse,
    process_thai,
)
from pythainlp.ulmfit.preprocess import (
    fix_html,
    lowercase_all,
    remove_space,
    replace_rep_after,
    replace_rep_nonum,
    replace_url,
    replace_wrep_post,
    replace_wrep_post_nonum,
    rm_brackets,
    rm_useless_newlines,
    rm_useless_spaces,
    spec_add_spaces,
    ungroup_emoji,
)
from pythainlp.ulmfit.tokenizer import BaseTokenizer as base_tokenizer

# pythainlp
from pythainlp.ulmfit import *


class TestUlmfitPackage(unittest.TestCase):
    def test_ThaiTokenizer(self):
        self.thai = ThaiTokenizer()
        self.assertIsNotNone(self.thai.tokenizer("ทดสอบการตัดคำ"))
        self.assertIsNone(self.thai.add_special_cases(["แมว"]))

    def test_BaseTokenizer(self):
        self.base = base_tokenizer(lang="th")
        self.assertIsNotNone(self.base.tokenizer("ทดสอบ การ ตัด คำ"))
        self.assertIsNone(self.base.add_special_cases(["แมว"]))

    def test_load_pretrained(self):
        self.assertIsNotNone(THWIKI_LSTM)

    def test_pre_rules_th(self):
        self.assertIsNotNone(pre_rules_th)

    def test_post_rules_th(self):
        self.assertIsNotNone(post_rules_th)

    def test_pre_rules_th_sparse(self):
        self.assertIsNotNone(pre_rules_th_sparse)

    def test_post_rules_th_sparse(self):
        self.assertIsNotNone(post_rules_th_sparse)

    def test_fix_html(self):
        self.assertEqual(
            fix_html("Some HTML&nbsp;text<br />"), "Some HTML& text\n"
        )

    def test_rm_useless_spaces(self):
        self.assertEqual(
            rm_useless_spaces("Inconsistent   use  of     spaces."),
            "Inconsistent use of spaces.",
        )

    def test_spec_add_spaces(self):
        self.assertEqual(
            spec_add_spaces("I #like to #put #hashtags #everywhere!"),
            "I  # like to  # put  # hashtags  # everywhere!",
        )

    def test_replace_rep_after(self):
        self.assertEqual(replace_rep_after("น้อยยยยยยยย"), "น้อยxxrep8 ")

    def test_replace_rep_nonum(self):
        self.assertEqual(replace_rep_nonum("น้อยยยยยยยย"), "น้อย xxrep ")

    def test_replace_wrep_post(self):
        self.assertEqual(
            replace_wrep_post(["น้อย", "น้อย"]), ["xxwrep", "1", "น้อย"]
        )

        self.assertEqual(
            replace_wrep_post(["นก", "กา", "กา", "กา"]),
            ["นก", "xxwrep", "2", "กา"],
        )

    def test_replace_wrep_post_nonum(self):
        self.assertEqual(
            replace_wrep_post_nonum(["น้อย", "น้อย"]), ["xxwrep", "น้อย"]
        )

        self.assertEqual(
            replace_wrep_post_nonum(["นก", "กา", "กา", "กา"]),
            ["นก", "xxwrep", "กา"],
        )

    def test_remove_space(self):
        self.assertEqual(remove_space([" ", "น้อย", " ", "."]), ["น้อย", "."])

    def test_replace_url(self):
        self.assertEqual(replace_url("https://thainlp.org web"), "xxurl web")

    def test_rm_useless_newlines(self):
        self.assertEqual(rm_useless_newlines("text\n\n"), "text ")

    def test_rm_brackets(self):
        self.assertEqual(rm_brackets("()()(ข้อความ)"), "(ข้อความ)")
        self.assertEqual(rm_brackets("[][][ข้อความ]"), "[ข้อความ]")
        self.assertEqual(rm_brackets("{}{}{ข้อความ}"), "{ข้อความ}")

    def test_ungroup_emoji(self):
        self.assertEqual(ungroup_emoji("👍👍👍"), ["👍", "👍", "👍"])

    def test_lowercase_all(self):
        self.assertEqual(
            lowercase_all("HeLlO ."), ["h", "e", "l", "l", "o", " ", "."]
        )

    def test_process_thai_sparse(self):
        text = "👍👍👍 #AnA มากกกก น้อยน้อย ().1146"

        actual = process_thai(text)

        # after pre_rules_th_sparse
        # >>> "👍👍👍 # Ana มาก xxrep  น้้อยน้อย .1146"
        #
        # after tokenize with word_tokenize(engine="newmm")
        # >>> ["👍👍👍", " ", "#", " ","Ana", " ", "มาก", "xxrep",
        #      "  ", "น้อย", "น้อย", " ", ".", "1146"]
        #
        # after post_rules_th
        # - remove whitespace token (" ")
        # >>> ["xxwrep, "👍", "#", "ana", "มาก",
        #       "xxrep", "xxwrep", "น้อย", ".", "1146"]

        expect = [
            "xxwrep",
            "👍",
            "#",
            "ana",
            "มาก",
            "xxrep",
            "xxwrep",
            "น้อย",
            ".",
            "1146",
        ]

        self.assertEqual(actual, expect)

    def test_process_thai_dense(self):
        text = "👍👍👍 #AnA มากกกก น้อยน้อย ().1146"

        actual = process_thai(
            text,
            pre_rules=pre_rules_th,
            post_rules=post_rules_th,
            tok_func=THAI2FIT_TOKENIZER.word_tokenize,
        )

        # after pre_rules_th
        # >>> "👍👍👍 # Ana มากxxrep4 น้้อยน้อย .1146"
        #
        # after tokenize with word_tokenize(engine="newmm")
        # >>> ["👍👍👍", " ", "#", "Ana", " ", "มาก", "xxrep", "4",
        #             " ", "น้อย", "น้อย", " ", ".", "1146"]
        # after post_rules_th
        # -- because it performs `replace_wrep_post` before `ungroup_emoji`,
        #    3 repetitive emoji are not marked with special token "xxwrep num"
        #
        # >>> ["👍", "👍","👍", " ", "#", "ana", " ", "มาก",
        #       "xxrep", "4", " ", "xxwrep", "1", "น้อย", " ",
        #       ".", "1146"]

        expect = [
            "👍",
            "👍",
            "👍",
            " ",
            "#",
            " ",
            "ana",
            " ",
            "มาก",
            "xxrep",
            "4",
            " ",
            "xxwrep",
            "1",
            "น้อย",
            " ",
            ".",
            "1146",
        ]

        self.assertEqual(actual, expect)

    def test_document_vector(self):
        imdb = untar_data(URLs.IMDB_SAMPLE)
        dummy_df = pd.read_csv(imdb / "texts.csv")
        thwiki = THWIKI_LSTM
        thwiki_itos = pickle.load(open(thwiki["itos_fname"], "rb"))
        thwiki_vocab = fastai.text.transform.Vocab(thwiki_itos)
        tt = Tokenizer(
            tok_func=ThaiTokenizer,
            lang="th",
            pre_rules=pre_rules_th,
            post_rules=post_rules_th,
        )
        processor = [
            TokenizeProcessor(
                tokenizer=tt, chunksize=10000, mark_fields=False
            ),
            NumericalizeProcessor(
                vocab=thwiki_vocab, max_vocab=60000, min_freq=3
            ),
        ]
        data_lm = (
            TextList.from_df(
                dummy_df, imdb, cols=["text"], processor=processor
            )
            .split_by_rand_pct(0.2)
            .label_for_lm()
            .databunch(bs=64)
        )
        data_lm.sanity_check()
        config = {
            "emb_sz": 400,
            "n_hid": 1550,
            "n_layers": 4,
            "pad_token": 1,
            "qrnn": False,
            "tie_weights": True,
            "out_bias": True,
            "output_p": 0.25,
            "hidden_p": 0.1,
            "input_p": 0.2,
            "embed_p": 0.02,
            "weight_p": 0.15,
        }
        trn_args = {"drop_mult": 0.9, "clip": 0.12, "alpha": 2, "beta": 1}
        learn = language_model_learner(
            data_lm, AWD_LSTM, config=config, pretrained=False, **trn_args
        )
        learn.load_pretrained(**thwiki)
        self.assertIsNotNone(document_vector("วันนี้วันดีปีใหม่", learn, data_lm))
        self.assertIsNotNone(
            document_vector("วันนี้วันดีปีใหม่", learn, data_lm, agg="sum")
        )
        with self.assertRaises(ValueError):
            document_vector("วันนี้วันดีปีใหม่", learn, data_lm, agg="abc")

    def test_merge_wgts(self):
        wgts = {"0.encoder.weight": torch.randn(5, 3)}
        itos_pre = ["แมว", "คน", "หนู"]
        itos_new = ["ปลา", "เต่า", "นก"]
        em_sz = 3
        self.assertIsNotNone(merge_wgts(em_sz, wgts, itos_pre, itos_new))
