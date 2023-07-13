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

class Chat:
    def __init__(self):
        pass
    def load_model(self, model_path,load_in_8bit=False,offload_folder="./",**):
        if model_path == "wangchanglm":
            from pythainlp.generate.wangchanglm import WangChanGLM
            self.model = WangChanGLM()
            self.model.load_model(
                model_path="pythainlp/wangchanglm-7.5B-sft-en-8bit-sharded",
                load_in_8bit=load_in_8bit,
                offload_folder=offload_folder,
                **
            )