# -*- coding: utf-8 -*-
import unittest
from pythainlp.ancient import aksonhan_to_current


class TestAncientPackage(unittest.TestCase):
    def test_aksonhan_to_current(self):
        self.assertEquals(aksonhan_to_current("ก"), 'ก')
        self.assertEquals(aksonhan_to_current("กก"), 'กก')
        self.assertEquals(aksonhan_to_current("ถนน"), 'ถนน')
        self.assertEquals(aksonhan_to_current("จกก"), 'จัก')
        self.assertEquals(aksonhan_to_current("ดง่ง"), 'ดั่ง')
        self.assertEquals(aksonhan_to_current("นน้น"), 'นั้น')
        self.assertEquals(aksonhan_to_current("ขดด"), 'ขัด')
        self.assertEquals(aksonhan_to_current("ตรสส"), 'ตรัส')
        self.assertEquals(aksonhan_to_current("ขบบ"), 'ขับ')
        self.assertEquals(aksonhan_to_current("วนน"), 'วัน')
        self.assertEquals(aksonhan_to_current("หลงง"), 'หลัง')
        self.assertEquals(aksonhan_to_current("บงงคบบ"), 'บังคับ')
        self.assertEquals(aksonhan_to_current("สรรเพชญ"), 'สรรเพชญ')
