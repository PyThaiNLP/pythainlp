# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai Grapheme-to-Phoneme (Thai G2P) v4

Hugging Face: https://huggingface.co/pythainlp/thaig2p-v4
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Optional

from pythainlp.corpus import get_hf_hub
from pythainlp.tools import safe_path_join

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray
    from onnxruntime import InferenceSession

_REPO_ID: str = "pythainlp/thaig2p-v4"
_MAX_LEN: int = 80
_PAD_TOKEN: int = 0
_SOS_TOKEN: int = 1
_EOS_TOKEN: int = 2
_UNK_TOKEN: int = 3


class ThaiG2P:
    """Thai Grapheme-to-Phoneme using ONNX model (v4).

    This version uses the pythainlp/thaig2p-v4 model based on ONNX
    for converting Thai text to International Phonetic Alphabet (IPA) representation.

    For more information, see:
    https://huggingface.co/pythainlp/thaig2p-v4
    """

    _encoder_session: InferenceSession
    _decoder_session: InferenceSession
    _input_char2idx: dict[str, int]
    _target_idx2char: dict[int, str]
    _max_len: int

    def __init__(
        self,
        providers: Optional[list[str]] = None,
        model_path: Optional[str] = None,
    ) -> None:
        """Initialize Thai G2P v4 model.

        :param Optional[list[str]] providers: ONNX runtime execution providers
            (default is ``['CPUExecutionProvider']``).
        :param Optional[str] model_path: Hugging Face model repository or local directory path
            (default is ``'pythainlp/thaig2p-v4'``).
        """
        try:
            import numpy as np  # noqa: F401
            import onnxruntime as ort
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "Please install the required packages via "
                "'pip install numpy onnxruntime huggingface-hub'."
            ) from exc

        if providers is None:
            providers = ["CPUExecutionProvider"]

        self._max_len = _MAX_LEN

        if model_path is not None and os.path.isdir(model_path):
            vocab_file = safe_path_join(model_path, "vocab.json")
            encoder_file = safe_path_join(model_path, "encoder_thaig2p.onnx")
            decoder_file = safe_path_join(model_path, "decoder_thaig2p.onnx")
        else:
            repo_id = model_path if model_path is not None else _REPO_ID
            vocab_file = get_hf_hub(repo_id, "vocab.json")
            encoder_file = get_hf_hub(repo_id, "encoder_thaig2p.onnx")
            decoder_file = get_hf_hub(repo_id, "decoder_thaig2p.onnx")

        with open(vocab_file, "r", encoding="utf-8") as f:
            vocab_data = json.load(f)

        self._input_char2idx = vocab_data["input_char2idx"]
        self._target_idx2char = {
            int(k): v for k, v in vocab_data["target_idx2char"].items()
        }

        self._encoder_session = ort.InferenceSession(
            encoder_file, providers=providers
        )
        self._decoder_session = ort.InferenceSession(
            decoder_file, providers=providers
        )

    def _encode_input(self, text: str) -> "NDArray[np.int64]":
        """Encode input text into padded token index sequence.

        :param str text: Thai text.
        :return: 2D array of token indices with shape (1, _max_len).
        :rtype: numpy.ndarray
        """
        import numpy as np

        src_indices = (
            [_SOS_TOKEN]
            + [self._input_char2idx.get(c, _UNK_TOKEN) for c in text]
            + [_EOS_TOKEN]
        )
        if len(src_indices) < self._max_len:
            src_indices += [_PAD_TOKEN] * (self._max_len - len(src_indices))
        else:
            src_indices = src_indices[: self._max_len]

        return np.array([src_indices], dtype=np.int64)

    def g2p(self, text: str) -> str:
        """Transliterate Thai text to IPA using G2P v4 model.

        :param str text: Thai text to be transliterated.
        :return: IPA transcription.
        :rtype: str
        """
        if not text or not isinstance(text, str):
            return ""

        import numpy as np

        src_tensor = self._encode_input(text)
        enc_outputs = self._encoder_session.run(
            output_names=["memory", "src_pad_mask"],
            input_feed={"src": src_tensor},
        )
        memory, src_pad_mask = enc_outputs

        trg_indices: list[int] = [_SOS_TOKEN]
        for _ in range(self._max_len):
            trg_padded = trg_indices + [_PAD_TOKEN] * (
                self._max_len - len(trg_indices)
            )
            trg_tensor = np.array([trg_padded[: self._max_len]], dtype=np.int64)
            dec_outputs = self._decoder_session.run(
                output_names=["output", "cross_attention"],
                input_feed={
                    "trg": trg_tensor,
                    "memory": memory,
                    "src_pad_mask": src_pad_mask,
                },
            )
            output = dec_outputs[0]
            current_step_idx = len(trg_indices) - 1
            next_token_logits = output[0, current_step_idx, :]
            next_token = int(np.argmax(next_token_logits))
            if next_token == _EOS_TOKEN:
                break
            trg_indices.append(next_token)
            if len(trg_indices) >= self._max_len:
                break

        result_chars = [
            self._target_idx2char.get(idx, "<UNK>")
            for idx in trg_indices[1:]
        ]
        return "".join(result_chars)


_THAI_G2P: Optional[ThaiG2P] = None


def transliterate(
    text: str,
    providers: Optional[list[str]] = None,
    model_path: Optional[str] = None,
) -> str:
    """Transliterate Thai text using Thai G2P v4 model.

    :param str text: Thai text to be transliterated.
    :param Optional[list[str]] providers: ONNX runtime execution providers
        (default is ``['CPUExecutionProvider']``).
    :param Optional[str] model_path: Hugging Face model repository or local directory path
        (default is ``'pythainlp/thaig2p-v4'``).
    :return: IPA transcription.
    :rtype: str
    """
    global _THAI_G2P
    if _THAI_G2P is None:
        _THAI_G2P = ThaiG2P(providers=providers, model_path=model_path)
    return _THAI_G2P.g2p(text)


ThaiG2PV4 = ThaiG2P

__all__: list[str] = [
    "ThaiG2P",
    "ThaiG2PV4",
    "transliterate",
]

