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
import re
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class WangChanGLM:
    def __init__(self):
        self.exclude_pattern = re.compile(r'[^ก-๙]+')
        self.PROMPT_DICT = {
            "prompt_input": (
                "<context>: {input}\n<human>: {instruction}\n<bot>: "
            ),
            "prompt_no_input": (
                "<human>: {instruction}\n<bot>: "
            ),
        }
    def is_exclude(self, text):
        return bool(self.exclude_pattern.search(text))
    def load_model(
        self,
        model_path,
        return_dict=True,
        load_in_8bit=False,
        device_map="auto",
        torch_dtype=torch.float16,
        offload_folder="./",
        low_cpu_mem_usage=True,
        **
    ):
        self.model_path = model_path
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path
            return_dict=return_dict,
            load_in_8bit=load_in_8bit,
            device_map=device_map,
            torch_dtype=torch_dtype,
            offload_folder=offload_folder,
            low_cpu_mem_usage=low_cpu_mem_usage,
            **
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.df = pd.DataFrame(self.tokenizer.vocab.items(), columns=['text', 'idx'])
        self.df['is_exclude'] = self.df.text.map(self.is_exclude)
        self.exclude_ids = self.df[self.df.is_exclude==True].idx.tolist()
    def gen_instruct(
        self,
        text,
        max_new_tokens=512,
        top_p=0.95,
        temperature=0.9,
        top_k=50,
        no_repeat_ngram_size=2,
        typical_p=1.
    ):
        batch = self.tokenizer(text, return_tensors="pt")
        with torch.cuda.amp.autocast(): # cuda -> cpu if cpu
            if Thai=="Yes":
                output_tokens = self.model.generate(
                    input_ids=batch["input_ids"],
                    max_new_tokens=max_new_tokens, # 512
                    begin_suppress_tokens = self.exclude_ids,
                    no_repeat_ngram_size=no_repeat_ngram_size,
                    #oasst k50
                    top_k=top_k,
                    top_p=top_p, # 0.95
                    typical_p=typical_p,
                    temperature=temperature, # 0.9
                )
            else:
                output_tokens = self.model.generate(
                    input_ids=batch["input_ids"],
                    max_new_tokens=max_new_tokens, # 512
                    no_repeat_ngram_size=no_repeat_ngram_size,
                    #oasst k50
                    top_k=top_k,
                    top_p=top_p, # 0.95
                    typical_p=typical_p,
                    temperature=temperature, # 0.9
                )
        return self.tokenizer.decode(output_tokens[0][len(batch["input_ids"][0]):], skip_special_tokens=True)
    def instruct_generate(
        self,
        instruct: str,
        context: str = None,
        max_gen_len=512,
        temperature: float =0.9,
        top_p: float = 0.95,
        top_k=50,
        no_repeat_ngram_size=2,
        typical_p=1
    ):
        if context == None or context=="":
            prompt = self.PROMPT_DICT['prompt_no_input'].format_map(
                {'instruction': instruct, 'input': ''}
            )
        else:
            prompt = self.PROMPT_DICT['prompt_input'].format_map(
                {'instruction': instruct, 'input': context}
            )
        result = self.gen_instruct(
            prompt,
            max_gen_len=max_gen_len,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            no_repeat_ngram_size=no_repeat_ngram_size,
            typical_p=typical_p
        )
        return result