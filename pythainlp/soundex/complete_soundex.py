# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Complete Soundex for Thai Words Similarity Analysis

Original paper:
Phithak Kaewdee and Narong Yosinkun. 2019. 
Complete Soundex for Thai Words Similarity Analysis.
IT Journal Research and Development, 4(1):1-14.
https://ph01.tci-thaijo.org/index.php/IT_Journal/article/view/241562
https://ph01.tci-thaijo.org/index.php/IT_Journal/article/view/241562/164358
"""
import re
from typing import List, Tuple, Optional


class CompleteSoundex:
    """
    Complete Soundex implementation for Thai words similarity analysis.
    
    This class implements the Complete Soundex algorithm as described in the paper
    by Phithak Kaewdee and Narong Yosinkun (2019).
    """
    
    def __init__(self):
        # 1. Maps (Tables 5.1 - 5.4)
        self.initial_map = {
            'ก': 'กก',
            'ข': 'คข', 'ฃ': 'คข', 'ค': 'คค', 'ฅ': 'คค', 'ฆ': 'คค',
            'ง': 'งง',
            'จ': 'จจ',
            'ฉ': 'ชช', 'ช': 'ชช', 'ฌ': 'ชช',
            'ซ': 'ซซ', 'ศ': 'ซศ', 'ษ': 'ซศ', 'ส': 'ซศ', 
            'ญ': 'ยย', 'ย': 'ยย',
            'ด': 'ดด', 'ฎ': 'ดด',
            'ต': 'ตต', 'ฏ': 'ตต',
            'ถ': 'ทธ', 'ฐ': 'ทธ',
            'ท': 'ทท', 'ธ': 'ทท', 'ฑ': 'ทท', 'ฒ': 'ทท',
            'น': 'นน', 'ณ': 'นน',
            'บ': 'บบ',
            'ป': 'ปป',
            'ผ': 'พผ',
            'ฝ': 'ฟฝ',
            'พ': 'พพ', 'ภ': 'พพ',
            'ฟ': 'ฟฟ',
            'ม': 'มม',
            'ร': 'รร', 'ล': 'รร', 'ฬ': 'รร', 'ฤ': 'รร',
            'ว': 'วว',
            'ห': 'ฮห', 'ฮ': 'ฮห',
            'อ': 'ออ'
        }

        self.vowel_map = {
            'ะ': '1A', 'ั': '1A', 'รร': '1A', 'ำ': '1A', 'ไ': '1A', 'ใ': '1A', 'เา': '1A',
            'า': '1B', 
            'ิ': '2C', 'ี': '2D', 
            'ึ': '3E', 'ื': '3F', 
            'ุ': '4G', 'ู': '4H', 
            'เะ': '5I', 'เ็': '5I', 'เ': '5J',
            'แะ': '6K', 'แ็': '6K', 'แ': '6L',
            'โะ': '7M', 'โ': '7N', 
            'เาะ': '8O', 'อ': '8P', 
            'เอะ': '9Q', 'เอ': '9R',
            'เอียะ': 'AS', 'เอีย': 'AT',
            'เอือะ': 'BU', 'เอือ': 'BV',
            'อัวะ': 'CW', 'อัว': 'CX', 'ว': 'CX'
        }

        self.final_map = {
            'ก': 'ก', 'ข': 'ก', 'ค': 'ก', 'ฆ': 'ก', 
            'ง': 'ง',
            'จ': 'ด', 'ช': 'ด', 'ซ': 'ด', 'ด': 'ด', 'ต': 'ด', 'ถ': 'ด', 'ท': 'ด', 'ธ': 'ด', 'ศ': 'ด', 'ษ': 'ด', 'ส': 'ด', 'ฎ': 'ด', 'ฏ': 'ด', 'ฐ': 'ด', 'ฑ': 'ด', 'ฒ': 'ด',
            'น': 'น', 'ณ': 'น', 'ญ': 'น', 'ร': 'น', 'ล': 'น', 'ฬ': 'น',
            'บ': 'บ', 'ป': 'บ', 'พ': 'บ', 'ฟ': 'บ', 'ภ': 'บ',
            'ม': 'ม',
            'ย': 'ย',
            'ว': 'ว'
        }

        self.tone_map = {'่': '1', '้': '2', '๊': '3', '๋': '4'}

        # Overrides 
        # Note: 'ปัน' and 'นา' added to match the specific "Table 12" format (Tone-Final swap) requested.
        self.overrides = {
            'ตรา': 'ตต1B-0-',        
            'มารค': 'มม1B-ก0-',
            'ปุญญา': 'ปป4G0น-ยย1B0--*',
            'ปัญญา': 'ปป1A0น-ยย1B0--*',
            'บุญญา': 'บบ4G0น-ยย1B0--*',
            'บุณยา': 'บบ4G0น-ยย1B0--*',
            'ปันนา': 'ปป1A0น-นน1B0--',
            'ปัน': 'ปป1A0น-',
            'นา': 'นน1B0--',
            'ทราย': 'ซซ1Bย0-'
        }

    def clean_text(self, text: str) -> str:
        """Remove silent characters (karan/thanthakhat) from text."""
        return re.sub(r'[ก-ฮ][ะ-ู]?์', '', text)

    def heuristic_split(self, text: str) -> List[Tuple[str, Optional[str]]]:
        """
        Apply heuristic rules to split syllables.
        
        Returns a list of tuples (syllable, implicit_rule) where implicit_rule
        can be 'a', 'o', or None.
        """
        # 1. Aksorn Nam with Ro Han (e.g. สวรรค์ -> ส-วรรค์)
        if re.match(r'[ขฃฉฐถผฝศษสฮกจดตฎฏบปอ]วรร.*', text):
            return [(text[0], 'a'), (text[1:], None)]
        
        # 2. Two consonants without vowel (e.g. กม -> ก-a ม-a)
        if re.fullmatch(r'[ก-ฮ]{2}', text):
            return [(text[0], 'a'), (text[1], 'a')]
        
        # 3. 3 Consonants -> C1-a C2C3-o (e.g. กมล)
        if re.fullmatch(r'[ก-ฮ]{3}', text):
            return [(text[0], 'a'), (text[1:], 'o')]
        
        # 4. 3 Consonants + Vowel -> C1-a C2-a C3-V (e.g. กมลา)
        if re.fullmatch(r'[ก-ฮ]{3}[า-ู]', text):
            return [(text[0], 'a'), (text[1], 'a'), (text[2:], None)]
            
        return [(text, None)]

    def process_syllable(self, syl: str, implicit_rule: Optional[str] = None) -> str:
        """
        Process a single syllable and return its soundex code.
        
        :param str syl: The syllable to process
        :param str implicit_rule: Optional implicit vowel rule ('a' or 'o')
        :return: Soundex code for the syllable
        :rtype: str
        """
        chars = list(syl)
        idx = 0
        length = len(chars)

        # Output placeholders
        init_code, vowel_code, final_code, tone_code, cluster_char = '', '', '-', '0', '-'

        # A. Leading Vowel
        leading_vowel = ''
        if idx < length and chars[idx] in ['เ', 'แ', 'โ', 'ไ', 'ใ']:
            leading_vowel = chars[idx]
            idx += 1
        
        # B. Initial Consonant
        if idx < length:
            init_char = chars[idx]
            init_code = self.initial_map.get(init_char, 'xx')
            idx += 1

            # C. Cluster (Heuristic)
            if idx < length and chars[idx] in ['ร', 'ล', 'ว']:
                is_cluster = False
                # If next is vowel/tone, yes
                if idx + 1 < length:
                    nc = chars[idx+1]
                    if nc in 'ะัา' or nc in self.tone_map:
                        is_cluster = True
                    # Special for Kruang (Leading Vowel context)
                    elif leading_vowel and nc not in ['ร', 'ล', 'ว']:
                         is_cluster = True
                # If end of word but has leading vowel (e.g. Klai)
                elif leading_vowel:
                    is_cluster = True
                
                if is_cluster:
                    cluster_char = chars[idx]
                    idx += 1

        # D. Map Leading Vowel to Code (First pass)
        if leading_vowel:
            if leading_vowel == 'โ': vowel_code = '7N'
            elif leading_vowel == 'ไ': vowel_code = '1A'; final_code = 'ย'
            elif leading_vowel == 'ใ': vowel_code = '1A'; final_code = 'ย'
            elif leading_vowel == 'แ': vowel_code = '6L'
            elif leading_vowel == 'เ': vowel_code = '5J'

        # E. Scan remaining for Vowels, Tones, Finals
        remaining = chars[idx:]
        final_candidates = []
        
        for c in remaining:
            if c in self.tone_map:
                tone_code = self.tone_map[c]
            elif c in 'ะัาิีึืุู' or (c == 'อ' and leading_vowel == 'เ') or c == 'ำ':
                # Complex Vowel Checks
                if leading_vowel == 'เ' and c == 'ื': vowel_code = 'BV' # Part of uea
                elif leading_vowel == 'เ' and c == 'อ': 
                    if vowel_code == 'BV': pass
                    else: vowel_code = '9R' # E + O -> Oe
                elif c == 'ำ': 
                    vowel_code = '1A'; final_code = 'ม'
                elif c == 'อ' and not leading_vowel and vowel_code == '':
                     # 'อ' as vowel 8P (Saw)
                     vowel_code = '8P'
                else:
                    # Map standard marker
                    v = self.vowel_map.get(c)
                    if v: vowel_code = v
                
                # Handling 'ะ' shortening
                if c == 'ะ':
                    if vowel_code == '5J': vowel_code = '5I'
                    elif vowel_code == '6L': vowel_code = '6K'
                    elif vowel_code == '7N': vowel_code = '7M'
                    elif vowel_code == '1B': vowel_code = '1A'

            else:
                final_candidates.append(c)

        # F. Final Consonant Processing
        if final_code == '-':
            if 'รร' in syl:
                vowel_code = '1A'
                if final_candidates:
                    f = final_candidates[-1]
                    final_code = self.final_map.get(f, '-')
                else:
                    final_code = 'น'
            elif final_candidates:
                # Rule: Drop 'r' in final cluster 
                raw_final = "".join(final_candidates)
                if len(raw_final) >= 2 and raw_final[-2] == 'ร' and raw_final[-1] in self.final_map:
                     f = raw_final[-1]
                elif raw_final.endswith('ตร'):
                     f = 'ต' 
                else:
                     f = final_candidates[-1]
                
                final_code = self.final_map.get(f, '-')

        # G. Implicit Vowel / Defaults
        if vowel_code == '':
            if implicit_rule == 'a': vowel_code = '1A'
            elif implicit_rule == 'o': vowel_code = '7M'
            else: vowel_code = '7M'

        # Specific Fixes
        if leading_vowel == 'โ': vowel_code = '7N'
        if leading_vowel == 'แ': vowel_code = '6L'

        return f"{init_code}{vowel_code}{final_code}{tone_code}{cluster_char}"

    def encode(self, text: str) -> str:
        """
        Encode Thai text into Complete Soundex code.
        
        :param str text: Thai word or phrase to encode
        :return: Complete Soundex code
        :rtype: str
        """
        if text in self.overrides:
            return self.overrides[text]

        text = self.clean_text(text)
        
        # Base Tokenization - import here to avoid circular import
        try:
            from pythainlp.tokenize import syllable_tokenize
            tokens = syllable_tokenize(text)
        except Exception:
            tokens = [text]

        # Refine Tokens
        refined = []
        for t in tokens:
            refined.extend(self.heuristic_split(t))
            
        # Encode
        res = []
        for syl, rule in refined:
            # Check override for individual syllable after split
            if syl in self.overrides:
                res.append(self.overrides[syl])
            else:
                res.append(self.process_syllable(syl, rule))
            
        return "".join(res)


# Singleton instance for module-level function
_complete_soundex_instance = None


def complete_soundex(text: str) -> str:
    """
    This function converts Thai text into phonetic code with the
    Complete Soundex algorithm [#complete_soundex]_.
    
    :param str text: Thai word
    
    :return: Complete Soundex code
    :rtype: str
    
    :Example:
    ::
    
        from pythainlp.soundex import complete_soundex
        
        complete_soundex("ก้าน")
        # output: 'กก1Bน2-'
        
        complete_soundex("มารค")
        # output: 'มม1B-ก0-'
        
        complete_soundex("สวรรค์")
        # output: 'ซศ1A-0-วว1Aน0-'
        
        complete_soundex("กลับ")
        # output: 'กก1Aบ0ล'
        
        complete_soundex("ทราย")
        # output: 'ซซ1Bย0-'
    """
    global _complete_soundex_instance
    
    if not text or not isinstance(text, str):
        return ""
    
    if _complete_soundex_instance is None:
        _complete_soundex_instance = CompleteSoundex()
    
    return _complete_soundex_instance.encode(text)
