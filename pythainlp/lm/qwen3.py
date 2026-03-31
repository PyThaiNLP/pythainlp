# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    import torch
    from transformers import PreTrainedModel, PreTrainedTokenizerBase


class Qwen3:
    """Qwen3-0.6B language model for Thai text generation.

    A small but capable language model from Alibaba Cloud's Qwen family,
    optimized for various NLP tasks including Thai language processing.
    """

    def __init__(self) -> None:
        self.model: Optional["PreTrainedModel"] = None
        self.tokenizer: Optional["PreTrainedTokenizerBase"] = None
        self.device: Optional[str] = None
        self.torch_dtype: Optional["torch.dtype"] = None
        self.model_path: Optional[str] = None

    def load_model(
        self,
        model_path: str = "Qwen/Qwen3-0.6B",
        device: str = "cuda",
        torch_dtype: Optional["torch.dtype"] = None,
        low_cpu_mem_usage: bool = True,
    ) -> None:
        """Load Qwen3 model.

        :param str model_path: model path or HuggingFace model ID
        :param str device: device (cpu, cuda or other)
        :param Optional[torch.dtype] torch_dtype: torch data type (e.g., torch.float16, torch.bfloat16)
        :param bool low_cpu_mem_usage: low cpu mem usage

        :Example:

            >>> from pythainlp.lm import Qwen3  # doctest: +SKIP
            >>> import torch  # doctest: +SKIP

            >>> model = Qwen3()  # doctest: +SKIP
            >>> model.load_model(device="cpu", torch_dtype=torch.bfloat16)  # doctest: +SKIP
        """
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except (ImportError, ModuleNotFoundError) as exc:
            raise ImportError(
                "Qwen3 language model requires optional dependencies. "
                "Install them with: pip install 'pythainlp[qwen3]'"
            ) from exc

        # Set default torch_dtype if not provided
        if torch_dtype is None:
            torch_dtype = torch.float16

        # Check CUDA availability early before loading model
        if device.startswith("cuda"):
            if not torch.cuda.is_available():
                raise RuntimeError(
                    "CUDA device requested but CUDA is not available. "
                    "Check your PyTorch installation and GPU drivers, or use "
                    "device='cpu' instead."
                )

        self.device = device
        self.torch_dtype = torch_dtype
        self.model_path = model_path

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to load tokenizer from '{self.model_path}'. "
                "Check the model path or your network connection."
            ) from exc

        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map=device,
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=low_cpu_mem_usage,
            )
        except OSError as exc:
            # Clean up tokenizer on failure
            self.tokenizer = None
            raise RuntimeError(
                f"Failed to load model from '{self.model_path}'. "
                "This can happen due to an invalid model path, missing files, "
                "or insufficient disk space."
            ) from exc
        except Exception as exc:
            # Clean up tokenizer on failure
            self.tokenizer = None
            raise RuntimeError(
                f"Failed to load model weights: {exc}. "
                "This can be caused by insufficient memory, an incompatible "
                "torch_dtype setting, or other configuration issues."
            ) from exc

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

            >>> from pythainlp.lm import Qwen3  # doctest: +SKIP
            >>> import torch  # doctest: +SKIP

            >>> model = Qwen3()  # doctest: +SKIP
            >>> model.load_model(device="cpu", torch_dtype=torch.bfloat16)  # doctest: +SKIP

            >>> result = model.generate("สวัสดี")  # doctest: +SKIP
            >>> print(result)  # doctest: +SKIP
        """
        if self.model is None or self.tokenizer is None or self.device is None:
            raise RuntimeError(
                "Model not loaded. Please call load_model() first."
            )

        if not text or not isinstance(text, str):
            raise ValueError("text parameter must be a non-empty string.")

        try:
            import torch
        except (ImportError, ModuleNotFoundError) as exc:
            raise ImportError(
                "Qwen3 language model requires optional dependencies. "
                "Install them with: pip install 'pythainlp[qwen3]'"
            ) from exc

        inputs = self.tokenizer(text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)

        # Note: When do_sample=False (greedy decoding), temperature, top_p,
        # and top_k parameters are ignored by the transformers library
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
        # output_ids and input_ids are guaranteed to be 2D tensors with
        # batch size 1 from the tokenizer call above
        generated_text = str(
            self.tokenizer.decode(
                output_ids[0][len(input_ids[0]) :],
                skip_special_tokens=skip_special_tokens,
            )
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

            >>> from pythainlp.lm import Qwen3  # doctest: +SKIP
            >>> import torch  # doctest: +SKIP

            >>> model = Qwen3()  # doctest: +SKIP
            >>> model.load_model(device="cpu", torch_dtype=torch.bfloat16)  # doctest: +SKIP

            >>> messages = [{"role": "user", "content": "สวัสดีครับ"}]  # doctest: +SKIP
            >>> response = model.chat(messages)  # doctest: +SKIP
            >>> print(response)  # doctest: +SKIP
        """
        if self.model is None or self.tokenizer is None or self.device is None:
            raise RuntimeError(
                "Model not loaded. Please call load_model() first."
            )

        if not messages or not isinstance(messages, list):
            raise ValueError(
                "messages parameter must be a non-empty list of message dictionaries."
            )

        # Apply chat template if available, otherwise format manually
        if hasattr(self.tokenizer, "apply_chat_template"):
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        else:
            # Simple fallback format - preserve content newlines
            lines = []
            for msg in messages:
                role = str(msg.get("role", "user")).replace("\n", " ")
                content = str(msg.get("content", ""))
                lines.append(f"{role}: {content}")
            text = "\n".join(lines) + "\nassistant: "

        try:
            import torch
        except (ImportError, ModuleNotFoundError) as exc:
            raise ImportError(
                "Qwen3 language model requires optional dependencies. "
                "Install them with: pip install 'pythainlp[qwen3]'"
            ) from exc

        inputs = self.tokenizer(text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)

        # Note: When do_sample=False (greedy decoding), temperature, top_p,
        # and top_k parameters are ignored by the transformers library
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
        # output_ids and input_ids are guaranteed to be 2D tensors with
        # batch size 1 from the tokenizer call above
        generated_text = str(
            self.tokenizer.decode(
                output_ids[0][len(input_ids[0]) :],
                skip_special_tokens=skip_special_tokens,
            )
        )

        return generated_text
