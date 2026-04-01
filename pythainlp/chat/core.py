# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import torch

    from pythainlp.generate.wangchanglm import WangChanGLM


class ChatBotModel:
    history: list[tuple[str, str]]
    model: "WangChanGLM"

    def __init__(self) -> None:
        """Chat using AI generation"""
        self.history = []

    def reset_chat(self) -> None:
        """Reset chat by cleaning history"""
        self.history = []

    def load_model(
        self,
        model_name: str = "wangchanglm",
        return_dict: bool = True,
        load_in_8bit: bool = False,
        device: str = "cuda",
        torch_dtype: Optional["torch.dtype"] = None,
        offload_folder: str = "./",
        low_cpu_mem_usage: bool = True,
    ) -> None:
        """Load model

        :param str model_name: Model name (Now, we support wangchanglm only)
        :param bool return_dict: return_dict
        :param bool load_in_8bit: load model in 8bit
        :param str device: device (cpu, cuda or other)
        :param Optional[torch.dtype] torch_dtype: torch_dtype
        :param str offload_folder: offload folder
        :param bool low_cpu_mem_usage: low cpu mem usage
        """
        import torch

        if torch_dtype is None:
            torch_dtype = torch.float16

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
                low_cpu_mem_usage=low_cpu_mem_usage,
            )
        else:
            raise NotImplementedError(f"We doesn't support {model_name}.")

    def chat(self, text: str) -> str:
        """Chatbot

        :param str text: text for asking chatbot with.
        :return: answer from chatbot.
        :rtype: str
        :Example:

            >>>     from pythainlp.chat import ChatBotModel  # doctest: +SKIP
            >>>     import torch  # doctest: +SKIP

            >>>     chatbot = ChatBotModel()  # doctest: +SKIP
            >>>     chatbot.load_model(device="cpu", torch_dtype=torch.bfloat16)  # doctest: +SKIP

            >>>     print(chatbot.chat("สวัสดี"))  # doctest: +SKIP
                ยินดีที่ได้รู้จัก

            >>>     print(chatbot.history)  # doctest: +SKIP
                [('สวัสดี', 'ยินดีที่ได้รู้จัก')]
        """
        _temp = ""
        if self.history:
            for h, b in self.history:
                _temp += (
                    self.model.PROMPT_DICT["prompt_chatbot"].format_map(
                        {"human": h, "bot": b}
                    )
                    + self.model.stop_token
                )
        _temp += self.model.PROMPT_DICT["prompt_chatbot"].format_map(
            {"human": text, "bot": ""}
        )
        _bot = self.model.gen_instruct(_temp)
        self.history.append((text, _bot))
        return _bot
