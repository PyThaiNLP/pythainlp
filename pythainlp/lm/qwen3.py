# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Any

import torch


class Qwen3:
    """Qwen3-0.6B language model for Thai text generation.

    A small but capable language model from Alibaba Cloud's Qwen family,
    optimized for various NLP tasks including Thai language processing.
    """

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self.torch_dtype = None
        self.model_path = None

    def load_model(
        self,
        model_path: str = "Qwen/Qwen3-0.6B",
        device: str = "cuda",
        torch_dtype=torch.float16,
        low_cpu_mem_usage: bool = True,
    ):
        """Load Qwen3 model.

        :param str model_path: model path or HuggingFace model ID
        :param str device: device (cpu, cuda or other)
        :param torch_dtype: torch data type (e.g., torch.float16, torch.bfloat16)
        :param bool low_cpu_mem_usage: low cpu mem usage

        :Example:
        ::

            from pythainlp.lm import Qwen3
            import torch

            model = Qwen3()
            model.load_model(device="cpu", torch_dtype=torch.bfloat16)
        """
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.device = device
        self.torch_dtype = torch_dtype
        self.model_path = model_path

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=low_cpu_mem_usage,
        )
        self.model.to(device)

    def generate(
        self,
        text: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        do_sample: bool = True,
        skip_special_tokens: bool = True,
    ) -> str:
        """Generate text from a prompt.

        :param str text: input text prompt
        :param int max_new_tokens: maximum number of new tokens to generate
        :param float temperature: temperature for sampling (higher = more random)
        :param float top_p: top p for nucleus sampling
        :param int top_k: top k for top-k sampling
        :param bool do_sample: whether to use sampling or greedy decoding
        :param bool skip_special_tokens: skip special tokens in output
        :return: generated text
        :rtype: str

        :Example:
        ::

            from pythainlp.lm import Qwen3
            import torch

            model = Qwen3()
            model.load_model(device="cpu", torch_dtype=torch.bfloat16)

            result = model.generate("สวัสดี")
            print(result)
        """
        if self.model is None or self.tokenizer is None or self.device is None:
            raise RuntimeError(
                "Model not loaded. Please call load_model() first."
            )

        inputs = self.tokenizer(text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)

        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=do_sample,
            )

        # Decode only the newly generated tokens
        generated_text = self.tokenizer.decode(
            output_ids[0][len(input_ids[0]) :],
            skip_special_tokens=skip_special_tokens,
        )

        return generated_text

    def chat(
        self,
        messages: list[dict[str, Any]],
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        do_sample: bool = True,
        skip_special_tokens: bool = True,
    ) -> str:
        """Generate text using chat format.

        :param list[dict[str, Any]] messages: list of message dictionaries with 'role' and 'content' keys
        :param int max_new_tokens: maximum number of new tokens to generate
        :param float temperature: temperature for sampling
        :param float top_p: top p for nucleus sampling
        :param int top_k: top k for top-k sampling
        :param bool do_sample: whether to use sampling
        :param bool skip_special_tokens: skip special tokens in output
        :return: generated response
        :rtype: str

        :Example:
        ::

            from pythainlp.lm import Qwen3
            import torch

            model = Qwen3()
            model.load_model(device="cpu", torch_dtype=torch.bfloat16)

            messages = [{"role": "user", "content": "สวัสดีครับ"}]
            response = model.chat(messages)
            print(response)
        """
        if self.model is None or self.tokenizer is None or self.device is None:
            raise RuntimeError(
                "Model not loaded. Please call load_model() first."
            )

        # Apply chat template if available, otherwise format manually
        if hasattr(self.tokenizer, "apply_chat_template"):
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        else:
            # Simple fallback format
            text = ""
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                text += f"{role}: {content}\n"
            text += "assistant: "

        inputs = self.tokenizer(text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)

        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=do_sample,
            )

        # Decode only the newly generated tokens
        generated_text = self.tokenizer.decode(
            output_ids[0][len(input_ids[0]) :],
            skip_special_tokens=skip_special_tokens,
        )

        return generated_text
