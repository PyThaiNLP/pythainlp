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
import torch


class ChatBotModel:
    def __init__(self):
        """
        Chat with AI generation
        """
        self.history = []
    def reset_chat(self):
        """
        Reset chat by clean history
        """
        self.history = []
    def load_model(
        self,
        model_name:str="wangchanglm",
        return_dict:bool=True,
        load_in_8bit:bool=False,
        device:str="cuda",
        torch_dtype=torch.float16,
        offload_folder:str="./",
        low_cpu_mem_usage:bool=True
    ):
        """
        Load model
        
        :param str model_name: Model name (Now, we support wangchanglm only)
        :param bool return_dict: return_dict
        :param bool load_in_8bit: load model in 8bit
        :param str device: device (cpu, cuda or other)
        :param torch_dtype torch_dtype: torch_dtype
        :param str offload_folder: offload folder
        :param bool low_cpu_mem_usage: low cpu mem usage
        """
        if model_name == "wangchanglm":
            from pythainlp.generate.wangchanglm import WangChanGLM
            self.model = WangChanGLM()
            self.model.load_model(
                model_path="pythainlp/wangchanglm-7.5B-sft-en-sharded",
                return_dict=return_dict,
                load_in_8bit=load_in_8bit,
                offload_folder=offload_folder,
                device=device,
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=low_cpu_mem_usage
            )
        else:
            raise NotImplementedError(f"We doesn't support {model_name}.")
    def chat(self, text:str)->str:
        """
        Chatbot
        
        :param str text: text for asking chatbot.
        :return: the answer from chatbot.
        :rtype: str
        :Example:
        ::

                from pythainlp.chat import ChatBotModel
                import torch

                chatbot = ChatBotModel()
                chatbot.load_model(device="cpu",torch_dtype=torch.bfloat16)

                print(chatbot.chat("สวัสดี"))
                # output: ยินดีที่ได้รู้จัก

                print(chatbot.history)
                # output: [('สวัสดี', 'ยินดีที่ได้รู้จัก')]
        """
        _temp=""
        if self.history!=[]:
            for h,b in self.history:
                _temp+=self.model.PROMPT_DICT['prompt_chatbot'].format_map({"human":h,"bot":b})+self.model.stop_token
        _temp+=self.model.PROMPT_DICT['prompt_chatbot'].format_map({"human":text,"bot":""})
        _bot = self.model.gen_instruct(_temp)
        self.history.append((text,_bot))
        return _bot
