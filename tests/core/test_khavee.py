# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.khavee import KhaveeVerifier

kv = KhaveeVerifier()


class KhaveeTestCase(unittest.TestCase):

    """Tests for KhaveeVerifier.check_sara, check_marttra, is_sumpus, check_klon, and check_aek_too methods."""

    def test_check_sara(self):
        """Test check_sara with basic, reduced, complex, embedded, and standalone character vowels."""
        # Basic Vowels
        self.assertEqual(kv.check_sara("ฉะ"), "อะ")
        self.assertEqual(kv.check_sara("ค่ะ"), "อะ")
        self.assertEqual(kv.check_sara("กระ"), "อะ")
        self.assertEqual(kv.check_sara("อรรถ"), "อะ")
        self.assertEqual(kv.check_sara("พาล"), "อา")
        self.assertEqual(kv.check_sara("พลา"), "อา")
        self.assertEqual(kv.check_sara("ฆาต"), "อา")
        self.assertEqual(kv.check_sara("ซ่า"), "อา")
        self.assertEqual(kv.check_sara("นิ"), "อิ")
        self.assertEqual(kv.check_sara("มิต"), "อิ")
        self.assertEqual(kv.check_sara("บิน"), "อิ")
        self.assertEqual(kv.check_sara("ยิ้ม"), "อิ")
        self.assertEqual(kv.check_sara("พิมพ์"), "อิ")
        self.assertEqual(kv.check_sara("หยิบ"), "อิ")
        self.assertEqual(kv.check_sara("ตรี"), "อี")
        self.assertEqual(kv.check_sara("ปี"), "อี")
        self.assertEqual(kv.check_sara("ปี่"), "อี")
        self.assertEqual(kv.check_sara("ฎี"), "อี")  # ทฤษฎี
        self.assertEqual(kv.check_sara("ตรี"), "อี")
        self.assertEqual(kv.check_sara("พลี"), "อี")
        self.assertEqual(kv.check_sara("นีย์"), "อี")
        self.assertEqual(kv.check_sara("ปรีดิ์"), "อี")
        self.assertEqual(kv.check_sara("ตรึก"), "อึ")
        self.assertEqual(kv.check_sara("ผึ้ง"), "อึ")
        self.assertEqual(kv.check_sara("อึ"), "อึ")
        self.assertEqual(kv.check_sara("ซึ้ง"), "อึ")
        self.assertEqual(kv.check_sara("ขึ้น"), "อึ")
        self.assertEqual(kv.check_sara("หนึ่ง"), "อึ")
        self.assertEqual(kv.check_sara("อึ่ง"), "อึ")
        self.assertEqual(kv.check_sara("อือ"), "อือ")
        self.assertEqual(kv.check_sara("มือ"), "อือ")
        self.assertEqual(kv.check_sara("ซื้อ"), "อือ")
        self.assertEqual(kv.check_sara("ปรือ"), "อือ")
        self.assertEqual(kv.check_sara("ธุ"), "อุ")
        self.assertEqual(kv.check_sara("ญุ"), "อุ")
        self.assertEqual(kv.check_sara("อุ๊ป"), "อุ")
        self.assertEqual(kv.check_sara("สุทธิ์"), "อุ")
        self.assertEqual(kv.check_sara("รุฬห์"), "อุ")
        self.assertEqual(kv.check_sara("ถู"), "อู")
        self.assertEqual(kv.check_sara("หรู"), "อู")
        self.assertEqual(kv.check_sara("ธูป"), "อู")
        self.assertEqual(kv.check_sara("กู้ด"), "อู")
        self.assertEqual(kv.check_sara("กูฏ"), "อู")
        self.assertEqual(kv.check_sara("บูรณ์"), "อู")
        self.assertEqual(kv.check_sara("กูณฑ์"), "อู")
        self.assertEqual(kv.check_sara("สูรย์"), "อู")
        self.assertEqual(kv.check_sara("เซะ"), "เอะ")
        self.assertEqual(kv.check_sara("เอ"), "เอ")
        self.assertEqual(kv.check_sara("เพช"), "เอ")
        self.assertEqual(kv.check_sara("เขษม"), "เอ")
        self.assertEqual(kv.check_sara("แอะ"), "แอะ")
        self.assertEqual(kv.check_sara("และ"), "แอะ")
        self.assertEqual(kv.check_sara("แประ"), "แอะ")
        self.assertEqual(kv.check_sara("แอ๊ะ"), "แอะ")
        self.assertEqual(kv.check_sara("แปร"), "แอ")
        self.assertEqual(kv.check_sara("แอร์"), "แอ")
        self.assertEqual(kv.check_sara("เรียน"), "เอีย")
        self.assertEqual(kv.check_sara("เกียร์"), "เอีย")
        self.assertEqual(kv.check_sara("เกียว"), "เอีย")
        self.assertEqual(kv.check_sara("เงือก"), "เอือ")
        self.assertEqual(kv.check_sara("เอือ"), "เอือ")
        self.assertEqual(kv.check_sara("เสือ"), "เอือ")
        self.assertEqual(kv.check_sara("เขือ"), "เอือ")
        self.assertEqual(kv.check_sara("กลัว"), "อัว")

        # Reduced and Transformed Vowels (สระลดรูป/เปลี่ยนรูป)
        self.assertEqual(kv.check_sara("อัน"), "อะ")
        self.assertEqual(kv.check_sara("กัน"), "อะ")
        self.assertEqual(kv.check_sara("สัญ"), "อะ")
        self.assertEqual(kv.check_sara("พวก"), "อัว")
        self.assertEqual(kv.check_sara("จวก"), "อัว")
        self.assertEqual(kv.check_sara("คน"), "โอะ")
        self.assertEqual(kv.check_sara("คล"), "โอะ")
        self.assertEqual(kv.check_sara("พร"), "ออ")
        self.assertEqual(kv.check_sara("วร"), "ออ")
        self.assertEqual(kv.check_sara("บวร"), "ออ")
        self.assertEqual(kv.check_sara("เป็น"), "เอะ")
        self.assertEqual(kv.check_sara("เจ็ด"), "เอะ")
        self.assertEqual(kv.check_sara("เผด็จ"), "เอะ")
        self.assertEqual(kv.check_sara("แข็ง"), "แอะ")
        self.assertEqual(kv.check_sara("แจ็ค"), "แอะ")
        self.assertEqual(kv.check_sara("แกร็น"), "แอะ")
        self.assertEqual(kv.check_sara("เลย"), "เออ")
        self.assertEqual(kv.check_sara("เริง"), "เออ")
        self.assertEqual(kv.check_sara("เดิน"), "เออ")
        self.assertEqual(kv.check_sara("เกิด"), "เออ")
        self.assertEqual(kv.check_sara("ล็อก"), "เอาะ")
        self.assertEqual(kv.check_sara("อ็อก"), "เอาะ")
        self.assertEqual(kv.check_sara("ก็"), "เอาะ")

        # Complex compound and hidden vowels
        self.assertEqual(kv.check_sara("ภูมิ"), "อู")  # ภูมิใจ (ไม่ใช่ ภู-มิ)
        self.assertEqual(kv.check_sara("เกียรติ"), "เอีย")
        self.assertEqual(kv.check_sara("เกตุ"), "เอ")
        self.assertEqual(kv.check_sara("เมรุ"), "เอ")
        self.assertEqual(kv.check_sara("เหตุ"), "เอ")
        self.assertEqual(kv.check_sara("ชาติ"), "อา")
        self.assertEqual(kv.check_sara("ญาติ"), "อา")
        self.assertEqual(kv.check_sara("ธาตุ"), "อา")
        self.assertEqual(kv.check_sara("พยาธิ"), "อา")
        self.assertEqual(kv.check_sara("วัติ"), "อะ")  # ประวัติ
        self.assertEqual(kv.check_sara("พรรดิ"), "อะ")  # จักรพรรดิ
        self.assertEqual(kv.check_sara("วรรดิ"), "อะ")  # จักรวรรดิ
        self.assertEqual(kv.check_sara("สมมุติ"), "อุ")
        self.assertEqual(kv.check_sara("ชาติ"), "อา")
        self.assertEqual(kv.check_sara("ชาติ"), "อา")

        self.assertEqual(kv.check_sara("ออ"), "ออ")
        self.assertEqual(kv.check_sara("ขอ"), "ออ")
        self.assertEqual(kv.check_sara("งอ"), "ออ")
        self.assertEqual(kv.check_sara("กรม"), "โอะ")
        self.assertEqual(kv.check_sara("อต"), "โอะ")
        self.assertEqual(kv.check_sara("อล"), "โอะ")
        self.assertEqual(kv.check_sara("ยศ"), "โอะ")
        self.assertEqual(kv.check_sara("โต๊ะ"), "โอะ")
        self.assertEqual(kv.check_sara("เร็จ"), "เอะ")
        self.assertEqual(kv.check_sara("แข็ง"), "แอะ")
        self.assertEqual(kv.check_sara("เตลิด"), "เออ")
        self.assertEqual(kv.check_sara("เหม่อ"), "เออ")
        self.assertEqual(kv.check_sara("เนย"), "เออ")
        self.assertEqual(kv.check_sara("เขนย"), "เออ")
        self.assertEqual(kv.check_sara("เพนียด"), "เอีย")
        self.assertEqual(kv.check_sara("เกลี้ยง"), "เอีย")
        self.assertEqual(kv.check_sara("อวก"), "อัว")
        self.assertEqual(kv.check_sara("ควร"), "อัว")
        self.assertEqual(kv.check_sara("เกลือ"), "เอือ")
        self.assertEqual(kv.check_sara("เรื่อง"), "เอือ")
        self.assertEqual(kv.check_sara("ธรรม"), "อำ")
        self.assertEqual(kv.check_sara("จำ"), "อำ")
        self.assertEqual(kv.check_sara("ผล็อย"), "เอาะ")

        # Vowels embedded with Karun (testing correct truncation before check)
        self.assertEqual(kv.check_sara("จันทร์"), "อะ")
        self.assertEqual(kv.check_sara("กษัตริย์"), "อะ")
        self.assertEqual(kv.check_sara("ลักษมณ์"), "อะ")
        self.assertEqual(kv.check_sara("ศาสตร์"), "อา")
        self.assertEqual(kv.check_sara("สินธุ์"), "อิ")
        self.assertEqual(kv.check_sara("ฟิล์ม"), "อิ")
        self.assertEqual(kv.check_sara("ทรีย์"), "อี")
        self.assertEqual(kv.check_sara("กอล์ฟ"), "ออ")
        self.assertEqual(kv.check_sara("เฮิรตซ์"), "เออ")

        # Standalone Character Vowels
        self.assertEqual(kv.check_sara("อ"), "อะ")
        self.assertEqual(kv.check_sara("ณ"), "อะ")
        self.assertEqual(kv.check_sara("ธ"), "อะ")
        self.assertEqual(kv.check_sara("พณ"), "อะ")
        self.assertEqual(kv.check_sara("บ"), "ออ")
        self.assertEqual(kv.check_sara("บ่"), "ออ")

        # ฤ / ฦ Phonemic Rules
        self.assertEqual(kv.check_sara("ฤทธิ์"), "อิ")
        self.assertEqual(kv.check_sara("กฤษ"), "อิ")
        self.assertEqual(kv.check_sara("กฤษณ์"), "อิ")
        self.assertEqual(kv.check_sara("ทฤษ"), "อิ")  # ทฤษฎี
        self.assertEqual(kv.check_sara("ฤกษ์"), "เออ")
        self.assertEqual(kv.check_sara("พฤษ"), "อึ")
        self.assertEqual(kv.check_sara("พฤติ"), "อึ")
        self.assertEqual(kv.check_sara("ฤดู"), "อึ")
        self.assertEqual(kv.check_sara("ฤา"), "อือ")
        self.assertEqual(kv.check_sara("ฤๅ"), "อือ")
        self.assertEqual(kv.check_sara("ฦา"), "อือ")
        self.assertEqual(kv.check_sara("ฦๅ"), "อือ")

    def test_check_marttra(self):
        """Test check_marttra for various final consonant patterns."""
        self.assertEqual(kv.check_marttra("ปลิง"), "กง")
        self.assertEqual(kv.check_marttra("ยูง"), "กง")
        self.assertEqual(kv.check_marttra("กล่อง"), "กง")
        self.assertEqual(kv.check_marttra("สอง"), "กง")
        self.assertEqual(kv.check_marttra("เอ็ง"), "กง")
        self.assertEqual(kv.check_marttra("งง"), "กง")
        self.assertEqual(kv.check_marttra("ผึ้ง"), "กง")
        self.assertEqual(kv.check_marttra("ซึ้ง"), "กง")
        self.assertEqual(kv.check_marttra("หนึ่ง"), "กง")
        self.assertEqual(kv.check_marttra("อึ่ง"), "กง")
        self.assertEqual(kv.check_marttra("แข็ง"), "กง")
        self.assertEqual(kv.check_marttra("เริง"), "กง")
        self.assertEqual(kv.check_marttra("เกลี้ยง"), "กง")
        self.assertEqual(kv.check_marttra("เรื่อง"), "กง")

        self.assertEqual(kv.check_marttra("ลม"), "กม")
        self.assertEqual(kv.check_marttra("เฉลิม"), "กม")
        self.assertEqual(kv.check_marttra("เข็ม"), "กม")
        self.assertEqual(kv.check_marttra("จาม"), "กม")
        self.assertEqual(kv.check_marttra("ยิ้ม"), "กม")
        self.assertEqual(kv.check_marttra("เกม"), "กม")
        self.assertEqual(kv.check_marttra("รมย์"), "กม")
        self.assertEqual(kv.check_marttra("พิมพ์"), "กม")
        self.assertEqual(kv.check_marttra("เขษม"), "กม")
        self.assertEqual(kv.check_marttra("ภูมิ"), "กม")
        self.assertEqual(kv.check_marttra("กรม"), "กม")
        self.assertEqual(kv.check_marttra("ธรรม"), "กม")
        self.assertEqual(kv.check_marttra("ฟิล์ม"), "กม")

        self.assertEqual(kv.check_marttra("สวย"), "เกย")
        self.assertEqual(kv.check_marttra("โปรย"), "เกย")
        self.assertEqual(kv.check_marttra("เนย"), "เกย")
        self.assertEqual(kv.check_marttra("คอย"), "เกย")
        self.assertEqual(kv.check_marttra("ง่าย"), "เกย")
        self.assertEqual(kv.check_marttra("ทัย"), "เกย")
        self.assertEqual(kv.check_marttra("เลื่อย"), "เกย")
        self.assertEqual(kv.check_marttra("เปื่อย"), "เกย")
        self.assertEqual(kv.check_marttra("เฉื่อย"), "เกย")
        self.assertEqual(kv.check_marttra("เหนื่อย"), "เกย")
        self.assertEqual(kv.check_marttra("เลย"), "เกย")
        self.assertEqual(kv.check_marttra("เขนย"), "เกย")
        self.assertEqual(kv.check_marttra("ผล็อย"), "เกย")

        self.assertEqual(kv.check_marttra("สาว"), "เกอว")
        self.assertEqual(kv.check_marttra("นิ้ว"), "เกอว")
        self.assertEqual(kv.check_marttra("แมว"), "เกอว")
        self.assertEqual(kv.check_marttra("ดาว"), "เกอว")
        self.assertEqual(kv.check_marttra("แก้ว"), "เกอว")
        self.assertEqual(kv.check_marttra("เกียว"), "เกอว")

        self.assertEqual(kv.check_marttra("บก"), "กก")
        self.assertEqual(kv.check_marttra("โรค"), "กก")
        self.assertEqual(kv.check_marttra("ลาก"), "กก")
        self.assertEqual(kv.check_marttra("นัข"), "กก")
        self.assertEqual(kv.check_marttra("จักร"), "กก")
        self.assertEqual(kv.check_marttra("ตรึก"), "กก")
        self.assertEqual(kv.check_marttra("เงือก"), "กก")
        self.assertEqual(kv.check_marttra("พวก"), "กก")
        self.assertEqual(kv.check_marttra("จวก"), "กก")
        self.assertEqual(kv.check_marttra("แจ็ค"), "กก")
        self.assertEqual(kv.check_marttra("ล็อก"), "กก")
        self.assertEqual(kv.check_marttra("อ็อก"), "กก")
        self.assertEqual(kv.check_marttra("อวก"), "กก")
        self.assertEqual(kv.check_marttra("ฤกษ์"), "กก")
        self.assertEqual(kv.check_marttra("ลักษมณ์"), "กก")

        self.assertEqual(kv.check_marttra("จด"), "กด")
        self.assertEqual(kv.check_marttra("ตรวจ"), "กด")
        self.assertEqual(kv.check_marttra("เสริฐ"), "กด")
        self.assertEqual(kv.check_marttra("บุตร"), "กด")
        self.assertEqual(kv.check_marttra("ตรุษ"), "กด")
        self.assertEqual(kv.check_marttra("มืด"), "กด")
        self.assertEqual(kv.check_marttra("โยชน์"), "กด")
        self.assertEqual(kv.check_marttra("ชาติ"), "กด")
        self.assertEqual(kv.check_marttra("เกียรติ"), "กด")
        self.assertEqual(kv.check_marttra("วรรดิ"), "กด")
        self.assertEqual(kv.check_marttra("สมมุติ"), "กด")
        self.assertEqual(kv.check_marttra("อรรถ"), "กด")
        self.assertEqual(kv.check_marttra("ฆาต"), "กด")
        self.assertEqual(kv.check_marttra("มิต"), "กด")
        self.assertEqual(kv.check_marttra("สุทธิ์"), "กด")
        self.assertEqual(kv.check_marttra("กู้ด"), "กด")
        self.assertEqual(kv.check_marttra("กูฏ"), "กด")
        self.assertEqual(kv.check_marttra("เพช"), "กด")
        self.assertEqual(kv.check_marttra("เจ็ด"), "กด")
        self.assertEqual(kv.check_marttra("เผด็จ"), "กด")
        self.assertEqual(kv.check_marttra("เกิด"), "กด")
        self.assertEqual(kv.check_marttra("เกตุ"), "กด")
        self.assertEqual(kv.check_marttra("เหตุ"), "กด")
        self.assertEqual(kv.check_marttra("ญาติ"), "กด")
        self.assertEqual(kv.check_marttra("ธาตุ"), "กด")
        self.assertEqual(kv.check_marttra("พยาธิ"), "กด")
        self.assertEqual(kv.check_marttra("วัติ"), "กด")
        self.assertEqual(kv.check_marttra("พรรดิ"), "กด")
        self.assertEqual(kv.check_marttra("อต"), "กด")
        self.assertEqual(kv.check_marttra("ยศ"), "กด")
        self.assertEqual(kv.check_marttra("เร็จ"), "กด")
        self.assertEqual(kv.check_marttra("เตลิด"), "กด")
        self.assertEqual(kv.check_marttra("เพนียด"), "กด")
        self.assertEqual(kv.check_marttra("กษัตริย์"), "กด")
        self.assertEqual(kv.check_marttra("ศาสตร์"), "กด")
        self.assertEqual(kv.check_marttra("เฮิรตซ์"), "กด")
        self.assertEqual(kv.check_marttra("ฤทธิ์"), "กด")
        self.assertEqual(kv.check_marttra("กฤษ"), "กด")
        self.assertEqual(kv.check_marttra("กฤษณ์"), "กด")
        self.assertEqual(kv.check_marttra("ทฤษ"), "กด")

        self.assertEqual(kv.check_marttra("มึน"), "กน")
        self.assertEqual(kv.check_marttra("ร้าน"), "กน")
        self.assertEqual(kv.check_marttra("ขนุน"), "กน")
        self.assertEqual(kv.check_marttra("คน"), "กน")
        self.assertEqual(kv.check_marttra("ทมิฬ"), "กน")
        self.assertEqual(kv.check_marttra("ซีน"), "กน")
        self.assertEqual(kv.check_marttra("บรร"), "กน")
        self.assertEqual(kv.check_marttra("กร"), "กน")
        self.assertEqual(kv.check_marttra("เณร"), "กน")
        self.assertEqual(kv.check_marttra("ยนต์"), "กน")
        self.assertEqual(kv.check_marttra("กรรณ"), "กน")
        self.assertEqual(kv.check_marttra("พาล"), "กน")
        self.assertEqual(kv.check_marttra("พาน"), "กน")
        self.assertEqual(kv.check_marttra("บิน"), "กน")
        self.assertEqual(kv.check_marttra("ขึ้น"), "กน")
        self.assertEqual(kv.check_marttra("รุฬห์"), "กน")
        self.assertEqual(kv.check_marttra("บูรณ์"), "กน")
        self.assertEqual(kv.check_marttra("กูณฑ์"), "กน")
        self.assertEqual(kv.check_marttra("สูรย์"), "กน")
        self.assertEqual(kv.check_marttra("เรียน"), "กน")
        self.assertEqual(kv.check_marttra("อัน"), "กน")
        self.assertEqual(kv.check_marttra("กัน"), "กน")
        self.assertEqual(kv.check_marttra("สัญ"), "กน")
        self.assertEqual(kv.check_marttra("คล"), "กน")
        self.assertEqual(kv.check_marttra("พร"), "กน")
        self.assertEqual(kv.check_marttra("วร"), "กน")
        self.assertEqual(kv.check_marttra("บวร"), "กน")
        self.assertEqual(kv.check_marttra("เป็น"), "กน")
        self.assertEqual(kv.check_marttra("แกร็น"), "กน")
        self.assertEqual(kv.check_marttra("เดิน"), "กน")
        self.assertEqual(kv.check_marttra("เมรุ"), "กน")
        self.assertEqual(kv.check_marttra("อล"), "กน")
        self.assertEqual(kv.check_marttra("ควร"), "กน")
        self.assertEqual(kv.check_marttra("จันทร์"), "กน")
        self.assertEqual(kv.check_marttra("สินธุ์"), "กน")

        self.assertEqual(kv.check_marttra("ชอบ"), "กบ")
        self.assertEqual(kv.check_marttra("ภาพ"), "กบ")
        self.assertEqual(kv.check_marttra("เทพ"), "กบ")
        self.assertEqual(kv.check_marttra("รูป"), "กบ")
        self.assertEqual(kv.check_marttra("เวฟ"), "กบ")
        self.assertEqual(kv.check_marttra("โลพ"), "กบ")
        self.assertEqual(kv.check_marttra("หยิบ"), "กบ")
        self.assertEqual(kv.check_marttra("อุ๊ป"), "กบ")
        self.assertEqual(kv.check_marttra("ธูป"), "กบ")
        self.assertEqual(kv.check_marttra("กอล์ฟ"), "กบ")

        self.assertEqual(kv.check_marttra("อะ"), "กา")
        self.assertEqual(kv.check_marttra("อา"), "กา")
        self.assertEqual(kv.check_marttra("อิ"), "กา")
        self.assertEqual(kv.check_marttra("อี"), "กา")
        self.assertEqual(kv.check_marttra("อึ"), "กา")
        self.assertEqual(kv.check_marttra("อือ"), "กา")
        self.assertEqual(kv.check_marttra("อุ"), "กา")
        self.assertEqual(kv.check_marttra("อู"), "กา")
        self.assertEqual(kv.check_marttra("เอะ"), "กา")
        self.assertEqual(kv.check_marttra("เอ"), "กา")
        self.assertEqual(kv.check_marttra("แอะ"), "กา")
        self.assertEqual(kv.check_marttra("แอ"), "กา")
        self.assertEqual(kv.check_marttra("โอะ"), "กา")
        self.assertEqual(kv.check_marttra("โอ"), "กา")
        self.assertEqual(kv.check_marttra("เอาะ"), "กา")
        self.assertEqual(kv.check_marttra("ออ"), "กา")
        self.assertEqual(kv.check_marttra("เอาะ"), "กา")
        self.assertEqual(kv.check_marttra("เออ"), "กา")
        self.assertEqual(kv.check_marttra("เอียะ"), "กา")
        self.assertEqual(kv.check_marttra("เอีย"), "กา")
        self.assertEqual(kv.check_marttra("เอือะ"), "กา")
        self.assertEqual(kv.check_marttra("เอือ"), "กา")
        self.assertEqual(kv.check_marttra("อัวะ"), "กา")
        self.assertEqual(kv.check_marttra("อัว"), "กา")
        self.assertEqual(kv.check_marttra("อำ"), "กา")
        self.assertEqual(kv.check_marttra("ไอ"), "กา")
        self.assertEqual(kv.check_marttra("ใอ"), "กา")
        self.assertEqual(kv.check_marttra("เอา"), "กา")
        self.assertEqual(kv.check_marttra("ปลา"), "กา")
        self.assertEqual(kv.check_marttra("งู"), "กา")
        self.assertEqual(kv.check_marttra("หมู"), "กา")
        self.assertEqual(kv.check_marttra("มือ"), "กา")
        self.assertEqual(kv.check_marttra("ล้อ"), "กา")
        self.assertEqual(kv.check_marttra("เมา"), "กา")
        self.assertEqual(kv.check_marttra("เหล้า"), "กา")
        self.assertEqual(kv.check_marttra("ฉะ"), "กา")
        self.assertEqual(kv.check_marttra("ค่ะ"), "กา")
        self.assertEqual(kv.check_marttra("กระ"), "กา")
        self.assertEqual(kv.check_marttra("พลา"), "กา")
        self.assertEqual(kv.check_marttra("ซ่า"), "กา")
        self.assertEqual(kv.check_marttra("นิ"), "กา")
        self.assertEqual(kv.check_marttra("ตริ"), "กา")
        self.assertEqual(kv.check_marttra("ปี"), "กา")
        self.assertEqual(kv.check_marttra("ปี่"), "กา")
        self.assertEqual(kv.check_marttra("ฎี"), "กา")
        self.assertEqual(kv.check_marttra("ตรี"), "กา")
        self.assertEqual(kv.check_marttra("พลี"), "กา")
        self.assertEqual(kv.check_marttra("ซื้อ"), "กา")
        self.assertEqual(kv.check_marttra("ปรือ"), "กา")
        self.assertEqual(kv.check_marttra("ธุ"), "กา")
        self.assertEqual(kv.check_marttra("ญุ"), "กา")
        self.assertEqual(kv.check_marttra("ถู"), "กา")
        self.assertEqual(kv.check_marttra("หรู"), "กา")
        self.assertEqual(kv.check_marttra("เซะ"), "กา")
        self.assertEqual(kv.check_marttra("เฉ"), "กา")
        self.assertEqual(kv.check_marttra("และ"), "กา")
        self.assertEqual(kv.check_marttra("แประ"), "กา")
        self.assertEqual(kv.check_marttra("แอ๊ะ"), "กา")
        self.assertEqual(kv.check_marttra("แอร์"), "กา")
        self.assertEqual(kv.check_marttra("เกียร์"), "กา")
        self.assertEqual(kv.check_marttra("เอือ"), "กา")
        self.assertEqual(kv.check_marttra("เสือ"), "กา")
        self.assertEqual(kv.check_marttra("เขือ"), "กา")
        self.assertEqual(kv.check_marttra("กลัว"), "กา")
        self.assertEqual(kv.check_marttra("ก็"), "กา")
        self.assertEqual(kv.check_marttra("ขอ"), "กา")
        self.assertEqual(kv.check_marttra("งอ"), "กา")
        self.assertEqual(kv.check_marttra("ขำ"), "กา")
        self.assertEqual(kv.check_marttra("จำ"), "กา")
        self.assertEqual(kv.check_marttra("โต๊ะ"), "กา")
        self.assertEqual(kv.check_marttra("เหม่อ"), "กา")
        self.assertEqual(kv.check_marttra("เกลือ"), "กา")
        self.assertEqual(kv.check_marttra("ตัว"), "กา")
        self.assertEqual(kv.check_marttra("ครัว"), "กา")
        self.assertEqual(kv.check_marttra("ทรีย์"), "กา")
        self.assertEqual(kv.check_marttra("ปรีดิ์"), "กา")
        self.assertEqual(kv.check_marttra("นีย์"), "กา")

        # Fake Finals (คำควบกล้า, คำที่มีพยัญชนะ/สระไม่ออกเสียง) mapping to open syllables
        self.assertEqual(kv.check_marttra("ไทย"), "กา")
        self.assertEqual(kv.check_marttra("ไกล"), "กา")
        self.assertEqual(kv.check_marttra("ใกล้"), "กา")
        self.assertEqual(kv.check_marttra("เสีย"), "กา")
        self.assertEqual(kv.check_marttra("เปล"), "กา")
        self.assertEqual(kv.check_marttra("ไกว"), "กา")
        self.assertEqual(kv.check_marttra("โปร"), "กา")
        self.assertEqual(kv.check_marttra("โปล"), "กา")
        self.assertEqual(kv.check_marttra("แปร"), "กา")
        self.assertEqual(kv.check_marttra("ไฟล์"), "กา")

        # Standalone Characters mapping to open syllables
        self.assertEqual(kv.check_marttra("ธ"), "กา")
        self.assertEqual(kv.check_marttra("ณ"), "กา")
        self.assertEqual(kv.check_marttra("พณ"), "กา")
        self.assertEqual(kv.check_marttra("บ"), "กา")
        self.assertEqual(kv.check_marttra("บ่"), "กา")
        self.assertEqual(kv.check_marttra("อ"), "กา")

        # ฤ / ฦ
        self.assertEqual(kv.check_marttra("ฤ"), "กา")
        self.assertEqual(kv.check_marttra("ฦ"), "กา")
        self.assertEqual(kv.check_marttra("ฤา"), "กา")
        self.assertEqual(kv.check_marttra("ฤๅ"), "กา")
        self.assertEqual(kv.check_marttra("ฦา"), "กา")
        self.assertEqual(kv.check_marttra("ฦๅ"), "กา")

    def test_is_sumpus(self):
        """Test is_sumpus for checking structural equivalence of Thai words."""
        self.assertFalse(kv.is_sumpus("สรร", "แมว"))
        self.assertFalse(kv.is_sumpus("กลัว", "ไกล"))
        self.assertFalse(kv.is_sumpus("ตัว", "ตะ"))
        self.assertFalse(kv.is_sumpus("ตัว", "ไต"))
        self.assertFalse(kv.is_sumpus("สาว", "อา"))
        self.assertFalse(kv.is_sumpus("เอว", "อา"))
        self.assertFalse(kv.is_sumpus("อัว", "อา"))
        self.assertFalse(kv.is_sumpus("บวก", "อัว"))
        self.assertFalse(kv.is_sumpus("สวม", "อัว"))
        self.assertFalse(kv.is_sumpus("ชัวร์", "ชัน"))
        self.assertFalse(kv.is_sumpus("เลว", "เร็ว"))
        self.assertFalse(kv.is_sumpus("ฤทธิ์", "ฤกษ์"))  # ฤทธิ์ = ริด, ฤกษ์ = เริก
        self.assertFalse(kv.is_sumpus("ฤทธิ์", "ลึด"))  # ฤทธิ์ = ริด != ลึด
        self.assertFalse(kv.is_sumpus("ฤกษ์", "ลึก"))  # ฤกษ์ = เริก != ลึก
        self.assertFalse(kv.is_sumpus("โหว่", "โถ่ว"))  # แม่ก กา vs แม่เกอว

        self.assertTrue(kv.is_sumpus("เขว", "เอ"))
        self.assertTrue(kv.is_sumpus("เขว", "เหว่"))
        self.assertTrue(kv.is_sumpus("เหว", "เอว"))
        self.assertTrue(kv.is_sumpus("โหว่", "โถ"))
        self.assertTrue(kv.is_sumpus("ครัว", "ตัว"))
        self.assertTrue(kv.is_sumpus("สรร", "อัน"))
        self.assertTrue(kv.is_sumpus("ธ", "ณ"))
        self.assertTrue(kv.is_sumpus("ธ", "ทะ"))
        self.assertTrue(kv.is_sumpus("ศาสตร์", "มารถ"))
        self.assertTrue(kv.is_sumpus("แตร", "แปร"))  # แม่ก กา
        self.assertTrue(kv.is_sumpus("แหล่", "แต่"))  # เหลือแหล่
        self.assertTrue(kv.is_sumpus("แหน", "แกน"))  # แม่ กน

        # Structural equivalence logic & Normalization
        self.assertTrue(kv.is_sumpus("บ้าน", "พาล"))
        self.assertTrue(kv.is_sumpus("ทำ", "จำ"))
        self.assertTrue(kv.is_sumpus("ทำ", "กัม"))
        self.assertTrue(kv.is_sumpus("กรรม", "ธรรม"))
        self.assertTrue(kv.is_sumpus("ธรรม", "สัม"))
        self.assertTrue(kv.is_sumpus("ธรรม", "จำ"))
        self.assertTrue(kv.is_sumpus("กัย", "ไก"))
        self.assertTrue(kv.is_sumpus("กัย", "ไกล"))
        self.assertTrue(kv.is_sumpus("ใจ", "ไทย"))
        self.assertTrue(kv.is_sumpus("ใจ", "จัย"))
        self.assertTrue(kv.is_sumpus("ไกว", "ใด"))
        self.assertTrue(kv.is_sumpus("ไกว", "ใคร"))
        self.assertTrue(kv.is_sumpus("เลย", "เกย"))
        self.assertTrue(kv.is_sumpus("พวก", "จวก"))
        self.assertTrue(kv.is_sumpus("ฤทธิ์", "กิด"))
        self.assertTrue(kv.is_sumpus("ฤกษ์", "เริก"))
        self.assertTrue(kv.is_sumpus("พฤษ", "พรึด"))
        self.assertTrue(kv.is_sumpus("พฤก", "พรึก"))
        self.assertTrue(kv.is_sumpus("ฤ", "รึ"))

        # Verify strict phonemic constraints are maintained
        self.assertFalse(kv.is_sumpus("ก็", "ก้อ"))  # เอาะ vs ออ

    def test_check_klon(self):
        """Test check_klon for Thai poem verification (k_type=4)."""
        self.assertEqual(
            kv.check_klon(
                "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง \
                    ลคคนเก่ง เอ๋งเอ๋งคะนอง มีคนจับจอง เขาชื่อน้องเธียร",
                k_type=4,
            ),
            "The poem is correct according to the principle.",
        )
        self.assertEqual(
            kv.check_klon(
                "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง \
                    ลคคนเก่ง เอ๋งเอ๋งเสียงหมา มีคนจับจอง เขาชื่อน้องเธียร",
                k_type=4,
            ),
            [
                "Can't find rhyme between paragraphs ('หมา', 'จอง') in paragraph 2",
                "Can't find rhyme between paragraphs ('หมา', 'ทอง') in paragraph 2",
            ],
        )

    def test_check_aek_too(self):
        """Test check_aek_too for Thai tone mark detection."""
        self.assertFalse(kv.check_aek_too("ไกด์"))
        self.assertEqual(kv.check_aek_too("ไก่"), "aek")
        self.assertEqual(kv.check_aek_too("ไก้"), "too")
        self.assertTrue(
            kv.check_aek_too(["หนม", "หน่ม", "หน้ม"]), [False, "aek", "too"]
        )


class KhaveeCheckKaruLahuTestCase(unittest.TestCase):

    """Tests for KhaveeVerifier.check_karu_lahu."""

    def setUp(self):
        """Set up test fixtures."""
        self.kv = KhaveeVerifier()

    def test_dead_syllable_is_karu(self):
        """Test that dead syllables are identified as karu."""
        self.assertEqual(self.kv.check_karu_lahu("กด"), "karu")

    def test_long_live_syllable_is_karu(self):
        """Test that long live syllables are identified as karu."""
        self.assertEqual(self.kv.check_karu_lahu("กา"), "karu")

    def test_live_syllable_with_final_consonant_is_karu(self):
        """Test that live syllables with final consonants are identified as karu."""
        self.assertEqual(self.kv.check_karu_lahu("กาน"), "karu")

    def test_bo_mai_ek_is_lahu(self):
        """Test that bo mai ek is identified as lahu."""
        self.assertEqual(self.kv.check_karu_lahu("บ่"), "lahu")

    def test_no_short_word_is_lahu(self):
        """Test that standalone consonant without vowel is identified as lahu."""
        self.assertEqual(self.kv.check_karu_lahu("ณ"), "lahu")

    def test_tho_short_word_is_lahu(self):
        """Test that tho short word is identified as lahu."""
        self.assertEqual(self.kv.check_karu_lahu("ธ"), "lahu")

    def test_ko_mai_is_lahu(self):
        """Test that ko mai (killed consonant marker) is identified as lahu."""
        self.assertEqual(self.kv.check_karu_lahu("ก็"), "lahu")


class KhaveeHandleKarunTestCase(unittest.TestCase):

    """Tests for KhaveeVerifier.handle_karun_sound_silence."""

    def setUp(self):
        """Set up test fixtures."""
        self.kv = KhaveeVerifier()

    def test_word_without_karun_unchanged(self):
        """Test that words without karun are unchanged."""
        self.assertEqual(self.kv.handle_karun_sound_silence("คน"), "คน")
        self.assertEqual(self.kv.handle_karun_sound_silence("กา"), "กา")
        # internal karun unchanged
        self.assertEqual(self.kv.handle_karun_sound_silence("การ์ตูน"), "การ์ตูน")
        self.assertEqual(self.kv.handle_karun_sound_silence("กอล์ฟ"), "กอล์ฟ")
        self.assertEqual(self.kv.handle_karun_sound_silence("ฟิล์ม"), "ฟิล์ม")
        self.assertEqual(self.kv.handle_karun_sound_silence("สตาร์ตอัป"), "สตาร์ตอัป")

    def test_word_ending_with_karun_stripped(self):
        """Test that karun and preceding consonant are stripped from end of word."""
        # เกมส์ → drop ์ and the consonant before it (ส) → เกม
        self.assertEqual(self.kv.handle_karun_sound_silence("เกมส์"), "เกม")

    def test_word_ending_with_karun_stripped_2(self):
        """Test karun stripping with different consonant."""
        # รักษ์ → drop ์ + ษ → รัก
        self.assertEqual(self.kv.handle_karun_sound_silence("รักษ์"), "รัก")

    def test_complex_karun_stripped(self):
        """Test complex karun stripping with single, multi-consonant, and vowel-embedded patterns."""
        # Explicit evaluation of single, multi-consonant, and vowel-embedded Karun rules
        self.assertEqual(self.kv.handle_karun_sound_silence("จันทร์"), "จัน")
        self.assertEqual(self.kv.handle_karun_sound_silence("สิทธิ์"), "สิท")
        self.assertEqual(self.kv.handle_karun_sound_silence("กษัตริย์"), "กษัต")
        self.assertEqual(self.kv.handle_karun_sound_silence("พระลักษมณ์"), "พระลัก")
        self.assertEqual(self.kv.handle_karun_sound_silence("อินทรีย์"), "อินทรี")
        self.assertEqual(self.kv.handle_karun_sound_silence("ภาพยนตร์"), "ภาพยน")
        self.assertEqual(self.kv.handle_karun_sound_silence("กาสาวพัสตร์"), "กาสาวพัส")
        self.assertEqual(self.kv.handle_karun_sound_silence("ไปรษณีย์"), "ไปรษณี")
        self.assertEqual(self.kv.handle_karun_sound_silence("สัปดาห์"), "สัปดา")
        self.assertEqual(self.kv.handle_karun_sound_silence("เฮิรตซ์"), "เฮิรต")
        self.assertEqual(self.kv.handle_karun_sound_silence("วิศวกรรมศาสตร์"), "วิศวกรรมศาส")
        self.assertEqual(self.kv.handle_karun_sound_silence("กบินทร์"), "กบิน")
        self.assertEqual(self.kv.handle_karun_sound_silence("นราธิเบนทร์"), "นราธิเบน")
        self.assertEqual(self.kv.handle_karun_sound_silence("พรหมจรรย์"), "พรหมจรร")
        self.assertEqual(self.kv.handle_karun_sound_silence("กรณีย์"), "กรณี")
        self.assertEqual(self.kv.handle_karun_sound_silence("รังสิมันตุ์"), "รังสิมัน")
        self.assertEqual(self.kv.handle_karun_sound_silence("รามเกียรติ์"), "รามเกียร")
        self.assertEqual(self.kv.handle_karun_sound_silence("ทรลักษณ์"), "ทรลัก")
        self.assertEqual(self.kv.handle_karun_sound_silence("ธำมรงค์"), "ธำมรง")
        self.assertEqual(self.kv.handle_karun_sound_silence("ศัพท์"), "ศัพ")
        self.assertEqual(self.kv.handle_karun_sound_silence("ฉันท์"), "ฉัน")
        self.assertEqual(self.kv.handle_karun_sound_silence("เจ้าเล่ห์"), "เจ้าเล่")
        self.assertEqual(self.kv.handle_karun_sound_silence("สงเคราะห์"), "สงเคราะ")
        self.assertEqual(self.kv.handle_karun_sound_silence("ราชทัณฑ์"), "ราชทัณ")
        self.assertEqual(self.kv.handle_karun_sound_silence("สวาสดิ์"), "สวาส")
        self.assertEqual(self.kv.handle_karun_sound_silence("สุปรีดิ์"), "สุปรี")

    def test_returns_string(self):
        """Test that handle_karun_sound_silence returns a string."""
        self.assertIsInstance(self.kv.handle_karun_sound_silence("สวัสดี"), str)


class KhaveeIsTrueFinalTestCase(unittest.TestCase):

    """Tests for internal method KhaveeVerifier._is_true_final."""

    def setUp(self):
        """Set up test fixtures."""
        self.kv = KhaveeVerifier()

    def test_true_finals(self):
        """Test identification of true final consonant patterns."""
        self.assertTrue(self.kv._is_true_final("จัย"))
        self.assertTrue(self.kv._is_true_final("สมัย"))
        self.assertTrue(self.kv._is_true_final("เลื่อย"))
        self.assertTrue(self.kv._is_true_final("เปื่อย"))
        self.assertTrue(self.kv._is_true_final("เฉื่อย"))
        self.assertTrue(self.kv._is_true_final("เหนื่อย"))

    def test_fake_finals(self):
        """Test identification of fake final consonant patterns."""
        self.assertFalse(self.kv._is_true_final("ไทย"))
        self.assertFalse(self.kv._is_true_final("ใคร"))
        self.assertFalse(self.kv._is_true_final("ไกล"))
        self.assertFalse(self.kv._is_true_final("ใกล้"))
        self.assertFalse(self.kv._is_true_final("เสีย"))
        self.assertFalse(self.kv._is_true_final("ไกว"))
        self.assertFalse(self.kv._is_true_final("โปร"))
        self.assertFalse(self.kv._is_true_final("แปร"))
        self.assertFalse(self.kv._is_true_final("เปล"))
        self.assertFalse(self.kv._is_true_final("ไฟล์"))


class KhaveeCheckAekTooEdgeCasesTestCase(unittest.TestCase):

    """Edge-case tests for KhaveeVerifier.check_aek_too."""

    def setUp(self):
        """Set up test fixtures."""
        self.kv = KhaveeVerifier()

    def test_non_string_raises_type_error(self):
        """Test that non-string input raises TypeError."""
        with self.assertRaises(TypeError):
            self.kv.check_aek_too(123)  # type: ignore[arg-type]

    def test_dead_syllable_as_aek_flag(self):
        """Test dead_syllable_as_aek flag behavior."""
        self.assertEqual(self.kv.check_aek_too("บท", dead_syllable_as_aek=True), "aek")

    def test_dead_syllable_without_flag_returns_false(self):
        """Test that dead syllables return False when flag is not set."""
        self.assertFalse(self.kv.check_aek_too("บท", dead_syllable_as_aek=False))

    def test_list_with_non_string_element_raises(self):
        """Test that list with non-string element raises TypeError."""
        with self.assertRaises(TypeError):
            self.kv.check_aek_too(["ไก่", 42])  # type: ignore[list-item]

    def test_both_tone_marks_returns_false(self):
        """Test that word with both tone marks returns False."""
        # word with both ่ and ้ should return False
        self.assertFalse(self.kv.check_aek_too("ก่้"))


class KhaveeCheckKlonExtendedTestCase(unittest.TestCase):

    """Tests for check_klon k_type=8 and invalid k_type."""

    def setUp(self):
        """Set up test fixtures."""
        self.kv = KhaveeVerifier()

    def test_invalid_k_type_returns_error_string(self):
        """Test that invalid k_type returns error string."""
        result = self.kv.check_klon("บทกวีทดสอบ", k_type=99)
        self.assertIsInstance(result, str)
        self.assertIn("Something went wrong", result)

    def test_incomplete_klon4_poem(self):
        """Test that incomplete klon4 poem is detected."""
        result = self.kv.check_klon("ฉันชื่อหมูกรอบ", k_type=4)
        self.assertIsInstance(result, str)
        self.assertIn("does not have 4 complete sentences", result)

    def test_incomplete_klon8_poem(self):
        """Test that incomplete klon8 poem is detected."""
        result = self.kv.check_klon("ฉันชื่อหมูกรอบ", k_type=8)
        self.assertIsInstance(result, str)

    def test_check_klon8_correct_poem(self):
        """Test that valid klon8 poem is recognized."""
        poem = (
            "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง "
            "ลคคนเก่ง เอ๋งเอ๋งคะนอง มีคนจับจอง เขาชื่อน้องเธียร"
        )
        self.assertIsNotNone(self.kv.check_klon(poem, k_type=8))

    def test_check_klon8_correct_poem_2(self):
        """Test that another valid klon8 poem is recognized."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารัก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือน จะจากเรือนร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        self.assertEqual(
            self.kv.check_klon(poem, k_type=8),
            "The poem is correct according to the principle."
        )

    def test_check_klon8_correct_poem_3(self):
        """Test that third valid klon8 poem is recognized."""
        poem = (
            "นางกอดจูบลูบหลังแล้วสั่งสอน อำนวยพรพลายน้อยละห้อยไห้ "
            "พ่อไปดีศรีสวัสดิ์กำจัดภัย จนเติบใหญ่ยิ่งยวดได้บวชเรียน "
            "ลูกผู้ชายลายมือนั้นคือยศ เเจ้าจงอตส่าห์ทำสม่ำเสมียน "
            "แล้วพาลูกออกมาข้างท่าเกวียน จะจากเจียนใจขาดอนาถใจ"
        )
        self.assertEqual(
            self.kv.check_klon(poem, k_type=8),
            "The poem is correct according to the principle."
        )

    def test_check_klon8_invalid_poem(self):
        """Test that invalid klon8 poem with too many words is detected."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารักมากมาก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือน จะจากเรือนร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, list)
        self.assertIn(
            "In sentence 2, there are more than 10 words. ['แม่', 'รัก', 'ลูก', 'ลูก', 'ก็', 'รู้', 'อยู่', 'ว่า', 'รัก', 'มาก', 'มาก']",
            result,
        )

    def test_check_klon8_invalid_poem_2(self):
        """Test that invalid klon8 poem with incorrect rhyme is detected."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารักมาก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือน จะจากเรือนร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, list)
        self.assertIn(
            "Can't find rhyme between paragraphs ('มาก', ['อื่น', 'สัก', 'หมื่น', 'แสน']) in paragraph 1",
            result,
        )

    def test_check_klon8_invalid_poem_3(self):
        """Test that invalid klon8 poem with wrong final word is detected."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารัก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือด จะจากเรือนร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, list)
        self.assertIn(
            "Can't find rhyme between paragraphs ('เหมือน', 'เตือด') in paragraph 1",
            result,
        )


class KhaveeCheckSaraEdgeCasesTestCase(unittest.TestCase):

    """Edge-case tests for KhaveeVerifier.check_sara."""

    def setUp(self):
        """Set up test fixtures."""
        self.kv = KhaveeVerifier()

    def test_bo_mai_ek_returns_oo(self):
        """Test that bo mai ek returns ออ vowel."""
        self.assertEqual(self.kv.check_sara("บ่"), "ออ")

    def test_special_word_เออ(self):
        """Test special word เออ vowel."""
        self.assertEqual(self.kv.check_sara("เออ"), "เออ")

    def test_special_word_เอ(self):
        """Test special word เอ vowel."""
        self.assertEqual(self.kv.check_sara("เอ"), "เอ")

    def test_special_word_เอะ(self):
        """Test special word เอะ vowel."""
        self.assertEqual(self.kv.check_sara("เอะ"), "เอะ")

    def test_special_word_เอา(self):
        """Test special word เอา vowel."""
        self.assertEqual(self.kv.check_sara("เอา"), "เอา")

    def test_special_word_เอาะ(self):
        """Test special word เอาะ vowel."""
        self.assertEqual(self.kv.check_sara("เอาะ"), "เอาะ")

    def test_ru_sara(self):
        """Test ฤ (ru) character vowel."""
        self.assertEqual(self.kv.check_sara("ฤ"), "อึ")

    def test_ruea_sara(self):
        """Test ฤา and ฤๅ (ru with aa vowel) characters."""
        # ฤา (ฤ + sara า U+0E32) → อือ; note: ฤๅ uses lakkhangyao, not sara aa
        self.assertEqual(self.kv.check_sara("ฤา"), "อือ")
        self.assertEqual(self.kv.check_sara("ฤๅ"), "อือ")

    def test_เอือ_sara(self):
        """Test เอือ vowel combination."""
        self.assertEqual(self.kv.check_sara("เรือ"), "เอือ")

    def test_returns_string(self):
        """Test that check_sara returns a string."""
        self.assertIsInstance(self.kv.check_sara("เริง"), str)
