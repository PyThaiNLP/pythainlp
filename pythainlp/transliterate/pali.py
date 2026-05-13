# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
import re


def pronunciate_pali(word: str) -> str:
    """
    Convert pali word to Thai pronunciation

    :param str word: Pali word (written in Thai script) to be pronunciated.

    :return: A string of Thai letters indicating
             how the input text should be pronounced.

    :Example:

        >>> from pythainlp.transliterate import pronunciate_pali
        >>> pronunciate_pali('ภควา')
        'ภะคะวา'
        >>> pronunciate_pali('สมฺมา')
        'สัมมา'
        >>> pronunciate_pali('มยํ')
        'มะยัง'
        >>> pronunciate_pali('สฺวากฺขา')
        'สวากขาโต'

    """
    # 1. จัดการช่องว่างที่อาจพิมพ์เกินมาก่อนนฤคหิต
    word = word.replace(" ํ", "ํ").replace("ฺ ", "ฺ")

    # --- กฎข้อ 3: นฤคหิต (ํ) ---
    # แบบมีสระหน้า (เ-ไ) เช่น โกํ -> โกง
    word = re.sub(r'([เ-ไ][ก-ฮ])ํ', r'\1ง_F_', word)      
    # แบบมีสระบน/ล่าง (ะ-ู) เช่น สุ ํ -> สุง
    word = re.sub(r'([ก-ฮ][ะ-ู])ํ', r'\1ง_F_', word)       
    # แบบพยัญชนะเดี่ยว เช่น หํ -> หัง
    word = re.sub(r'([ก-ฮ])ํ', r'\1ัง_F_', word)          

    # --- กฎข้อ 4 & 5: พินทุ (ฺ) เป็นตัวควบกล้ำ (ต้นคำ) ---
    # ถ้าพินทุอยู่พยัญชนะตัวแรกของคำ (ไม่มีตัวอื่นนำหน้า) ให้มาร์คเป็นตัวควบกล้ำ (_C_)
    word = re.sub(r'(^|\s)([ก-ฮ])ฺ', r'\1\2_C_', word)

    # --- กฎข้อ 2: พินทุ (ฺ) เป็นตัวสะกด ---
    # แบบมีสระนำหน้า เช่น เนยฺ -> เนย
    word = re.sub(r'([เ-ไ][ก-ฮ])([ก-ฮ])ฺ', r'\1\2_F_', word) 
    # แบบมีสระบน/ล่าง เช่น ทิฏฺ -> ทิฏ
    word = re.sub(r'([ก-ฮ][ะ-ู])([ก-ฮ])ฺ', r'\1\2_F_', word)  
    # แบบพยัญชนะเดี่ยว (สะกด) เช่น สมฺ -> สัม (เพิ่มไม้หันอากาศ)
    word = re.sub(r'([ก-ฮ])([ก-ฮ])ฺ', r'\1ั\2_F_', word)      

    # --- กฎข้อ 1: พยัญชนะที่ไม่มีเครื่องหมาย ให้อ่านเสียง "อะ" ---
    # หาพยัญชนะที่: ไม่ได้ตามหลัง เ-ไ และ ไม่ได้นำหน้าสระ, ไม่ใช่ตัวสะกด(_F_), ไม่ใช่ตัวควบ(_C_)
    word = re.sub(r'(?<![เ-ไ])([ก-ฮ])(?![ะ-ู็-์]|_F_|_C_)', r'\1ะ', word)

    # ทำความสะอาด Marker ที่เราใช้ทดไว้ตอนประมวลผล (_F_ = Final, _C_ = Cluster)
    word = word.replace('_F_', '').replace('_C_', '')

    return word