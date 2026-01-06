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

Note:
    This soundex algorithm is designed to work on individual Thai syllables.
    For best results, tokenize your text into words first using word_tokenize(),
    then into syllables using syllable_tokenize() before applying this soundex.
    
    Example:
        from pythainlp.tokenize import word_tokenize, syllable_tokenize
        from pythainlp.soundex import complete_soundex
        
        text = "สวัสดีครับ"
        words = word_tokenize(text)  # ['สวัสดี', 'ครับ']
        for word in words:
            syllables = syllable_tokenize(word)  # e.g., ['สะ', 'หวัด', 'ดี']
            for syllable in syllables:
                soundex_code = complete_soundex(syllable)
                print(f"{syllable} -> {soundex_code}")
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
        # Thai consonants for pattern matching
        self.thai_consonants = 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬฮอ'
        
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

    def clean_text(self, text: str) -> str:
        """Remove silent characters (karan/thanthakhat) from text."""
        return re.sub(r'[ก-ฮ][ะ-ู]?์', '', text)

    def heuristic_split(self, text: str) -> List[Tuple[str, Optional[str]]]:
        """
        Apply heuristic rules to split syllables.
        
        Returns a list of tuples (syllable, implicit_rule) where implicit_rule
        can be 'a', 'o', or None.
        """
        # 0. Handle อัต pattern (split as อัต-รา but keep ต with second syllable)
        if text.startswith('อัต') and len(text) > 3:
            # Split as อัต and ตX... (keep ต with the rest)
            return [('อัต', None), ('ต' + text[3:], None)]
        
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
        init_char = ''
        special_format = False  # For ญ/ย initial with tone-final swap

        # A. Leading Vowel
        leading_vowel = ''
        if idx < length and chars[idx] in ['เ', 'แ', 'โ', 'ไ', 'ใ']:
            leading_vowel = chars[idx]
            idx += 1
        
        # B. Initial Consonant
        if idx < length:
            init_char = chars[idx]
            
            # Special case: ทร- pattern should map to ซ initial
            if init_char == 'ท' and idx + 1 < length and chars[idx + 1] == 'ร':
                init_code = 'ซซ'  # ทร maps to ซซ
                idx += 2
                cluster_char = 'ร'  # ร is treated as cluster but not in output for this case
                # Actually for ทราย, we want ซซ with ร as cluster but special handling
                cluster_char = '-'  # Don't output cluster for ทร pattern
            else:
                init_code = self.initial_map.get(init_char, 'xx')
                idx += 1
                
                # Check for special tone-final format:
                # 1. If ญ/ย is the initial consonant in a syllable
                # 2. If the final consonant is ญ/น (from ญ)
                # We'll check the final later and set special_format then

                # C. Cluster (Heuristic)
                if idx < length and chars[idx] in ['ร', 'ล', 'ว']:
                    is_cluster = False
                    # Cluster detection: ร/ล/ว is a cluster if:
                    # 1. Followed by a vowel MARKER (not standalone vowel like า, เ, แ, etc.)
                    # 2. Or at end of word with leading vowel context
                    if idx + 1 < length:
                        nc = chars[idx+1]
                        # Only treat as cluster if followed by combining vowel marks or tones
                        if nc in 'ะัิีึืุู' or nc in self.tone_map:
                            is_cluster = True
                        # Special for Kruang with leading vowel
                        elif leading_vowel and nc not in ['ร', 'ล', 'ว'] and nc not in self.thai_consonants and nc != 'า':
                            is_cluster = True
                    # If end of word but has leading vowel (e.g. เกล)
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
        dropped_r = False  # Track if ร was dropped before final
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
                    dropped_r = True  # Mark that ร was dropped
                elif raw_final.endswith('ตร'):
                    f = 'ต' 
                    dropped_r = True  # Mark that ร was dropped
                else:
                    f = final_candidates[-1]
                
                final_code = self.final_map.get(f, '-')
        
        # Check if special format needed 
        # Special format (tone before final) is used when:
        # 1. Initial consonant is ญ, ย, or น
        # 2. Final consonant is ญ or ณ
        # 3. Final consonant is น AND vowel is short (1A vowel code)
        if init_char in ['ญ', 'ย', 'น']:
            special_format = True
        if final_candidates and any(c in ['ญ', 'ณ'] for c in final_candidates):
            special_format = True
        if final_candidates and any(c == 'น' for c in final_candidates) and vowel_code == '1A':
            special_format = True

        # G. Implicit Vowel / Defaults
        if vowel_code == '':
            if implicit_rule == 'a': vowel_code = '1A'
            elif implicit_rule == 'o': vowel_code = '7M'
            else: vowel_code = '7M'

        # Specific Fixes
        if leading_vowel == 'โ': vowel_code = '7N'
        if leading_vowel == 'แ': vowel_code = '6L'
        
        # H. Special adjustments for ส mapping
        # When 'ส' is split with implicit 'a', it should use ซศ (not ซซ)
        # ซซ is only for standalone 'ส' in complete syllables
        if init_char == 'ส' and init_code == 'ซศ':
            # Only change to ซซ if this is NOT an implicit split
            if implicit_rule is None and len(syl) >= 2:
                # Check if this is a simple syllable (just ส + vowel, no other consonants)
                consonants_after_init = [c for c in syl[1:] if 'ก' <= c <= 'ฮ']
                if not consonants_after_init or all(c in 'รลว' for c in consonants_after_init):
                    init_code = 'ซซ'

        # I. Format output - Standard vs Special format
        if special_format:
            # Special format: InitVowelToneFinalCluster (without asterisk here)
            # Swap tone and final positions
            result = f"{init_code}{vowel_code}{tone_code}{final_code}{cluster_char}"
        else:
            # Standard format: InitVowelFinalToneCluster
            # Add dash after vowel if:
            #   1. ร was dropped AND final is ก (velar), OR
            #   2. ร was dropped AND there's no final (final_code == '-')
            if dropped_r and (final_code == 'ก' or final_code == '-'):
                result = f"{init_code}{vowel_code}-{final_code}{tone_code}{cluster_char}"
            else:
                result = f"{init_code}{vowel_code}{final_code}{tone_code}{cluster_char}"
        
        return result

    def encode(self, text: str) -> str:
        """
        Encode a single Thai syllable into Complete Soundex code.
        
        Note:
            This method is designed to work on individual syllables.
            For multi-syllable words, tokenize into syllables first using
            syllable_tokenize() and call this method on each syllable separately.
        
        :param str text: Thai syllable to encode
        :return: Complete Soundex code
        :rtype: str
        
        :Example:
            >>> from pythainlp.soundex import complete_soundex
            >>> complete_soundex("ก้าน")
            'กก1Bน2-'
            
            For multi-syllable words:
            >>> from pythainlp.tokenize import syllable_tokenize
            >>> syllables = syllable_tokenize("สวัสดี")
            >>> codes = [complete_soundex(syl) for syl in syllables]
        """
        text = self.clean_text(text)
        
        if not text:
            return ""
        
        # Process as single syllable - apply heuristic splits if needed
        refined = self.heuristic_split(text)
        
        # Encode each part
        res = []
        for syl, rule in refined:
            res.append(self.process_syllable(syl, rule))
        
        result = "".join(res)
        
        # Add asterisk at the end for specific patterns:
        # 1. Contains ญญ (double ญ)
        # 2. Contains ญ and ย together
        # 3. Contains ณ and ย together  
        # 4. Starts with ญ (ญ as initial)
        if 'ญญ' in text or ('ญ' in text and 'ย' in text) or ('ณ' in text and 'ย' in text) or text.startswith('ญ'):
            result += '*'
            
        return result


# Singleton instance for module-level function
_complete_soundex_instance = None


def complete_soundex(text: str) -> str:
    """
    Convert a Thai syllable into phonetic code using the Complete Soundex algorithm.
    
    Note:
        This function is designed to work on individual Thai syllables.
        For multi-syllable words, tokenize into syllables first using
        syllable_tokenize() from pythainlp.tokenize.
    
    :param str text: Thai syllable
    
    :return: Complete Soundex code
    :rtype: str
    
    :Example:
    ::
    
        from pythainlp.soundex import complete_soundex
        
        # Single syllable encoding
        complete_soundex("ก้าน")
        # output: 'กก1Bน2-'
        
        complete_soundex("กลับ")
        # output: 'กก1Aบ0ล'
        
        # For multi-syllable words, tokenize first
        from pythainlp.tokenize import syllable_tokenize
        
        syllables = syllable_tokenize("สวรรค์")  # ['ส', 'วรรค์']
        codes = [complete_soundex(syl) for syl in syllables]
        # codes: ['ซศ1A-0-', 'วว1Aน0-']
        
        # Or combine syllables
        syllables = syllable_tokenize("ปันนา")  # ['ปัน', 'นา']
        result = ''.join([complete_soundex(syl) for syl in syllables])
        # result: 'ปป1A0น-นน1B0--'
    """
    global _complete_soundex_instance
    
    if not text or not isinstance(text, str):
        return ""
    
    if _complete_soundex_instance is None:
        _complete_soundex_instance = CompleteSoundex()
    
    return _complete_soundex_instance.encode(text)
