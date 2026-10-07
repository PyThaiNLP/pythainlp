# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Chatbot using the WangChanGLM model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pythainlp.tools import warn_deprecation

if TYPE_CHECKING:
    import torch

    from pythainlp.generate.wangchanglm import WangChanGLM


class ChatBotModel:
    """Chat with the WangChanGLM model."""

    history: list[tuple[str, str]]
    model: WangChanGLM

    def __init__(self) -> None:
        """Initialize the chatbot with an empty chat history."""
        self.history = []

    def reset_chat(self) -> None:
        """Reset the chat by clearing the history."""
        self.history = []

    def load_model(
        self,
        model_name: str = "wangchanglm",
        return_dict: bool = True,
        load_in_8bit: bool = False,
        device: str = "cuda",
        torch_dtype: Optional[torch.dtype] = None,
        offload_folder: str = "./",
        low_cpu_mem_usage: bool = True,
    ) -> None:
        """
        Load the model.

        :param str model_name: model name (only wangchanglm is supported)
        :param bool return_dict: return the output as a dictionary
        :param bool load_in_8bit: load the model in 8-bit precision
        :param str device: device (cpu, cuda, or other)
        :param Optional[torch.dtype] torch_dtype: data type of the model
        :param str offload_folder: folder to offload weights to
        :param bool low_cpu_mem_usage: reduce CPU memory usage while loading
        """
        warn_deprecation(
            "pythainlp.chat.ChatBotModel",
            deprecated_version="5.3.8",
            removal_version="6.0.0",
        )
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
        """
        Send a text to the chatbot and return its answer.

        :param str text: text to ask the chatbot
        :return: answer from the chatbot
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
