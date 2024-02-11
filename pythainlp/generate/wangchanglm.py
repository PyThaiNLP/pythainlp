# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
import re
import torch


class WangChanGLM:
    def __init__(self):
        self.exclude_pattern = re.compile(r'[^ก-๙]+')
        self.stop_token = "\n"
        self.PROMPT_DICT = {
            "prompt_input": (
                "<context>: {input}\n<human>: {instruction}\n<bot>: "
            ),
            "prompt_no_input": (
                "<human>: {instruction}\n<bot>: "
            ),
            "prompt_chatbot": (
                "<human>: {human}\n<bot>: {bot}"
            ),
        }
    def is_exclude(self, text:str)->bool:
        return bool(self.exclude_pattern.search(text))
    def load_model(
        self,
        model_path:str="pythainlp/wangchanglm-7.5B-sft-en-sharded",
        return_dict:bool=True,
        load_in_8bit:bool=False,
        device:str="cuda",
        torch_dtype=torch.float16,
        offload_folder:str="./",
        low_cpu_mem_usage:bool=True
    ):
        """
        Load model
        
        :param str model_path: model path
        :param bool return_dict: return dict
        :param bool load_in_8bit: load model in 8bit
        :param str device: device (cpu, cuda or other)
        :param torch_dtype torch_dtype: torch_dtype
        :param str offload_folder: offload folder
        :param bool low_cpu_mem_usage: low cpu mem usage
        """
        import pandas as pd
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.device = device
        self.torch_dtype = torch_dtype
        self.model_path = model_path
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            return_dict=return_dict,
            load_in_8bit=load_in_8bit,
            device_map=device,
            torch_dtype=torch_dtype,
            offload_folder=offload_folder,
            low_cpu_mem_usage=low_cpu_mem_usage
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.df = pd.DataFrame(self.tokenizer.vocab.items(), columns=['text', 'idx'])
        self.df['is_exclude'] = self.df.text.map(self.is_exclude)
        self.exclude_ids = self.df[self.df.is_exclude is True].idx.tolist()
    def gen_instruct(
        self,
        text:str,
        max_new_tokens:int=512,
        top_p:float=0.95,
        temperature:float=0.9,
        top_k:int=50,
        no_repeat_ngram_size:int=2,
        typical_p:float=1.,
        thai_only:bool=True,
        skip_special_tokens:bool=True
    ):
        """
        Generate Instruct
        
        :param str text: text
        :param int max_new_tokens: maximum number of new tokens
        :param float top_p: top p
        :param float temperature: temperature
        :param int top_k: top k
        :param int no_repeat_ngram_size: do not repeat ngram size
        :param float typical_p: typical p
        :param bool thai_only: Thai only
        :param bool skip_special_tokens: skip special tokens
        :return: the answer from Instruct
        :rtype: str
        """
        batch = self.tokenizer(text, return_tensors="pt")
        with torch.autocast(device_type=self.device, dtype=self.torch_dtype):
            if thai_only:
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
        return self.tokenizer.decode(output_tokens[0][len(batch["input_ids"][0]):], skip_special_tokens=skip_special_tokens)
    def instruct_generate(
        self,
        instruct: str,
        context: str = None,
        max_new_tokens=512,
        temperature: float =0.9,
        top_p: float = 0.95,
        top_k:int=50,
        no_repeat_ngram_size:int=2,
        typical_p:float=1,
        thai_only:bool=True,
        skip_special_tokens:bool=True
    ):
        """
        Generate Instruct
        
        :param str instruct: Instruct
        :param str context: context
        :param int max_new_tokens: maximum number of new tokens
        :param float top_p: top p
        :param float temperature: temperature
        :param int top_k: top k
        :param int no_repeat_ngram_size: do not repeat ngram size
        :param float typical_p: typical p
        :param bool thai_only: Thai only
        :param bool skip_special_tokens: skip special tokens
        :return: the answer from Instruct
        :rtype: str

        :Example:
        ::

                from pythainlp.generate.wangchanglm import WangChanGLM
                import torch

                model = WangChanGLM()

                model.load_model(device="cpu",torch_dtype=torch.bfloat16)

                print(model.instruct_generate(instruct="ขอวิธีลดน้ำหนัก"))
                # output: ลดน้ําหนักให้ได้ผล ต้องทําอย่างค่อยเป็นค่อยไป
                # ปรับเปลี่ยนพฤติกรรมการกินอาหาร
                # ออกกําลังกายอย่างสม่ําเสมอ
                # และพักผ่อนให้เพียงพอ
                # ที่สําคัญควรหลีกเลี่ยงอาหารที่มีแคลอรี่สูง
                # เช่น อาหารทอด อาหารมัน อาหารที่มีน้ําตาลสูง
                # และเครื่องดื่มแอลกอฮอล์

        """
        if context in (None, ""):
            prompt = self.PROMPT_DICT['prompt_no_input'].format_map(
                {'instruction': instruct, 'input': ''}
            )
        else:
            prompt = self.PROMPT_DICT['prompt_input'].format_map(
                {'instruction': instruct, 'input': context}
            )
        result = self.gen_instruct(
            prompt,
            max_new_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            no_repeat_ngram_size=no_repeat_ngram_size,
            typical_p=typical_p,
            thai_only=thai_only,
            skip_special_tokens=skip_special_tokens
        )
        return result
