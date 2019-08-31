# -*- coding: utf-8 -*-

import datetime
import os
import unittest

from pythainlp.ulmfit import (
    ThaiTokenizer,
    BaseTokenizer,
    fix_html,
    _THWIKI_LSTM,
    pre_rules_th,
    post_rules_th,
    rm_useless_spaces,
    spec_add_spaces,
    rm_useless_newlines,
    rm_brackets,
    ungroup_emoji,
    lowercase_all,
    replace_rep_nonum,
    replace_rep_after,
    replace_wrep_post,
    replace_wrep_post_nonum,
    remove_space
)


class TestUlmfitPackage(unittest.TestCase):

    def test_ThaiTokenizer(self):
        self.thai = ThaiTokenizer()
        self.assertIsNotNone(self.thai.tokenizer("ทดสอบการตัดคำ"))
        self.assertIsNone(self.thai.add_special_cases(["แมว"]))

    def test_BaseTokenizer(self):
        self.base = BaseTokenizer(lang='th')
        self.assertIsNotNone(self.base.tokenizer("ทดสอบ การ ตัด คำ"))
        self.assertIsNone(self.base.add_special_cases(["แมว"]))

    def test_load_pretrained(self):
        self.assertIsNotNone(_THWIKI_LSTM)

    def test_pre_rules_th(self):
        self.assertIsNotNone(pre_rules_th)

    def test_post_rules_th(self):
        self.assertIsNotNone(post_rules_th)

    def test_fix_html(self):
        self.assertEqual(
                fix_html("Some HTML&nbsp;text<br />"),
                "Some HTML& text\n")

    def test_rm_useless_spaces(self):
        self.assertEqual(
                rm_useless_spaces("Inconsistent   use  of     spaces."),
                "Inconsistent use of spaces.")

    def test_spec_add_spaces(self):
        self.assertEqual(
                spec_add_spaces("I #like to #put #hashtags #everywhere!"),
                "I  # like to  # put  # hashtags  # everywhere!")

    def test_replace_rep_after(self):
        self.assertEqual(
                replace_rep_after("น้อยยยยยยยย"),
                "น้อยxxrep8 ")

    def test_replace_rep_nonum(self):
        self.assertEqual(
                replace_rep_nonum("น้อยยยยยยยย"),
                "น้อย xxrep ")

    def test_replace_wrep_post(self):
        self.assertEqual(
                replace_wrep_post(["น้อย", "น้อย"]),
                ["xxwrep", "1", "น้อย"])

        self.assertEqual(
                replace_wrep_post(["นก", "กา", "กา", "กา"]),
                ["นก", "xxwrep", "2", "กา"])

    def test_replace_wrep_post_nonum(self):
        self.assertEqual(
                replace_wrep_post_nonum(["น้อย", "น้อย"]),
                ["xxwrep", "น้อย"])

        self.assertEqual(
                replace_wrep_post_nonum(["นก", "กา", "กา", "กา"]),
                ["นก", "xxwrep", "กา"])

    def test_remove_space(self):
        self.assertEqual(
                remove_space([" ", "น้อย", " ", "."]),
                ["น้อย", "."])

    def test_rm_useless_newlines(self):
        self.assertEqual(
                rm_useless_newlines("text\n\n"),
                "text ")

    def test_rm_brackets(self):
        self.assertEqual(
                rm_brackets("()()(ข้อความ)"),
                "(ข้อความ)")
        self.assertEqual(
                rm_brackets("[][][ข้อความ]"),
                "[ข้อความ]")
        self.assertEqual(
                rm_brackets("{}{}{ข้อความ}"),
                "{ข้อความ}")

    def test_ungroup_emoji(self):
        self.assertEqual(
                ungroup_emoji("👍👍👍"),
                ["👍", "👍", "👍"])

    def test_lowercase_all(self):
        self.assertEqual(
                lowercase_all("HeLlO ."),
                ['h', 'e', 'l', 'l', 'o', ' ', '.'])

