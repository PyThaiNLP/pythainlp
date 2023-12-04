# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List, Tuple, Collection, Callable
import re
import warnings
import random
from pythainlp.tokenize import word_tokenize
from transformers import (
    CamembertTokenizer,
)


_model_name = "clicknext/phayathaibert"
_tokenizer = CamembertTokenizer.from_pretrained(_model_name)

class ThaiTextProcessor:
    def __init__(self):
        self._TK_UNK, self._TK_REP, self._TK_WREP, self._TK_URL, self._TK_END = "<unk> <rep> <wrep> <url> </s>".split()
        self.SPACE_SPECIAL_TOKEN = "<_>"


    def replace_url(self, text: str) -> str:
        """
            Replace url in `text` with TK_URL (https://stackoverflow.com/a/6041965)
            :param str text: text to replace url
            :return: text where urls  are replaced
            :rtype: str
            :Example:
                >>> replace_url("go to https://github.com")
                go to <url>
        """
        URL_PATTERN = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
        return re.sub(URL_PATTERN, self._TK_URL, text)

    def rm_brackets(text: str) -> str:
        """
            Remove all empty brackets and artifacts within brackets from `text`.
            :param str text: text to remove useless brackets
            :return: text where all useless brackets are removed
            :rtype: str
            :Example:
                >>> rm_brackets("hey() whats[;] up{*&} man(hey)")
                hey whats up man(hey)
        """
        # remove empty brackets
        new_line = re.sub(r"\(\)", "", text)
        new_line = re.sub(r"\{\}", "", new_line)
        new_line = re.sub(r"\[\]", "", new_line)
        # brakets with only punctuations
        new_line = re.sub(r"\([^a-zA-Z0-9ก-๙]+\)", "", new_line)
        new_line = re.sub(r"\{[^a-zA-Z0-9ก-๙]+\}", "", new_line)
        new_line = re.sub(r"\[[^a-zA-Z0-9ก-๙]+\]", "", new_line)
        # artifiacts after (
        new_line = re.sub(r"(?<=\()[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line)
        new_line = re.sub(r"(?<=\{)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line)
        new_line = re.sub(r"(?<=\[)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line)
        # artifacts before )
        new_line = re.sub(r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\))", "", new_line)
        new_line = re.sub(r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\})", "", new_line)
        new_line = re.sub(r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\])", "", new_line)
        return new_line

    def replace_newlines(text: str) -> str:
        """
            Replace newlines in `text` with spaces.
            :param str text: text to replace all newlines with spaces
            :return: text where all newlines are replaced with spaces
            :rtype: str
            :Example:
                >>> rm_useless_spaces("hey whats\n\nup")
                hey whats  up
        """

        return re.sub(r"[\n]", " ", text.strip())

    def rm_useless_spaces(text: str) -> str:
        """
            Remove multiple spaces in `text`. (code from `fastai`)
            :param str text: text to replace useless spaces
            :return: text where all spaces are reduced to one
            :rtype: str
            :Example:
                >>> rm_useless_spaces("oh         no")
                oh no
        """
        return re.sub(" {2,}", " ", text)

    def replace_spaces(text: str, space_token: str = self.SPACE_SPECIAL_TOKEN) -> str:
        """
            Replace spaces with _
            :param str text: text to replace spaces
            :return: text where all spaces replaced with _
            :rtype: str
            :Example:
                >>> replace_spaces("oh no")
                oh_no
        """
        return re.sub(" ", space_token, text)

    def replace_rep_after(text: str) -> str:
        """
        Replace repetitions at the character level in `text`
        :param str text: input text to replace character repetition
        :return: text with repetitive tokens removed.
        :rtype: str
        :Example:
            >>> text = "กาาาาาาา"
            >>> replace_rep_after(text)
            'กา'
        """

        def _replace_rep(m):
            c, cc = m.groups()
            return f"{c}"

        re_rep = re.compile(r"(\S)(\1{3,})")
        return re_rep.sub(_replace_rep, text)

    def replace_wrep_post(toks: Collection[str]) -> Collection[str]:
        """
        Replace reptitive words post tokenization;
        fastai `replace_wrep` does not work well with Thai.
        :param Collection[str] toks: list of tokens
        :return: list of tokens where repetitive words are removed.
        :rtype: Collection[str]
        :Example:
            >>> toks = ["กา", "น้ำ", "น้ำ", "น้ำ", "น้ำ"]
            >>> replace_wrep_post(toks)
            ['กา', 'น้ำ']
        """
        previous_word = None
        rep_count = 0
        res = []
        for current_word in toks + [self._TK_END]:
            if current_word == previous_word:
                rep_count += 1
            elif (current_word != previous_word) & (rep_count > 0):
                res += [previous_word]
                rep_count = 0
            else:
                res.append(previous_word)
            previous_word = current_word
        return res[1:]

    def remove_space(toks: Collection[str]) -> Collection[str]:
        """
        Do not include space for bag-of-word models.
        :param Collection[str] toks: list of tokens
        :return: Collection of tokens where space tokens (" ") are filtered out
        :rtype: Collection[str]
        :Example:
            >>> toks = ['ฉัน','เดิน',' ','กลับ','บ้าน']
            >>> remove_space(toks)
            ['ฉัน','เดิน','กลับ','บ้าน']
        """
        res = []
        for t in toks:
            t = t.strip()
            if t:
                res.append(t)
        return res

    # combine them together
    def preprocess(
        self,
        text: str,
        pre_rules: Collection[Callable] = [
            rm_brackets,
            replace_newlines,
            rm_useless_spaces,
            replace_spaces,
            replace_rep_after,
        ],
        tok_func: Callable = word_tokenize,
    ) -> str:
        text = text.lower()
        for rule in pre_rules:
            text = rule(text)
        toks = tok_func(text)
        return "".join(toks)



class ThaiTextAugmenter:
    def __init__(self)->None:
        from transformers import (AutoTokenizer, 
                                  AutoModelForMaskedLM, 
                                  pipeline,)
        self.tokenizer = AutoTokenizer.from_pretrained(_model_name)
        self.model_for_masked_lm = AutoModelForMaskedLM.from_pretrained(_model_name)
        self.model = pipeline("fill-mask", tokenizer=self.tokenizer, model=self.model_for_masked_lm)
        self.processor = ThaiTextProcessor()

    def generate(self,
                 sample_text: str, 
                 word_rank: int, 
                 max_length: int=3,
                 sample: bool=False
                 )->str:
        sample_txt = sample_text
        final_text = ""
        for j in range(max_length):
            input = self.processor.preprocess(sample_txt)
            if sample:
                random_word_idx = random.randint(0, 4)
                output = self.model(input)[random_word_idx]['sequence']
            else:
                output = self.model(input)[word_rank]['sequence']
            sample_txt = output+"<mask>"
            final_text = sample_txt

        gen_txt = re.sub("<mask>","",final_text)
        return gen_txt
    

    def augment(self,
                text: str, 
                num_augs: int=3, 
                sample: bool=False
                )->List[str]:
        augment_list = []
        if num_augs <= 5: # since huggingface transformers pipeline default was set to 5 generated text
            for rank in range(num_augs):
                gen_text = self.generate(text, rank, sample=sample)
                processed_text = re.sub("<_>", " ", self.processor.preprocess(gen_text))
                augment_list.append(processed_text)

            return augment_list



class PartOfSpeechTagger:
    def __init__(self, model: str="lunarlist/pos_thai_phayathai") -> None:
        # Load model directly
        from transformers import (
            AutoTokenizer, 
            AutoModelForTokenClassification,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForTokenClassification.from_pretrained(model)

    def get_tag(self, sentence: str, strategy: str='simple')->List[List[Tuple[str, str]]]:
        from transformers import TokenClassificationPipeline
        pipeline = TokenClassificationPipeline(
            model=self.model, 
            tokenizer=self.tokenizer, 
            aggregation_strategy=strategy,
        )
        outputs = pipeline(sentence)
        word_tags = [[(tag['word'], tag['entity_group']) for tag in outputs]]
        return word_tags
    
def segment(sentence: str)->List[str]:
    if not sentence or not isinstance(sentence, str):
        return []

    return _tokenizer.tokenize(sentence)