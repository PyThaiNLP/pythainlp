# -*- coding: utf-8 -*-

import unittest

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
from pythainlp.ulmfit.tokenizer import BaseTokenizer


class TestUlmfitPackage(unittest.TestCase):
    def test_ThaiTokenizer(self):
        self.thai = ThaiTokenizer()
        self.assertIsNotNone(self.thai.tokenizer("ทดสอบการตัดคำ"))
        self.assertIsNone(self.thai.add_special_cases(["แมว"]))

    def test_BaseTokenizer(self):
        self.base = BaseTokenizer(lang="th")
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
