# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai Grapheme-to-Phoneme (Thai G2P) v3

GitHub: https://github.com/wannaphong/thai-g2p-v3
"""

from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING, Dict, List, Optional

from pythainlp.tools import get_full_data_path

_logger: logging.Logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray
    from onnxruntime import InferenceSession

_MODEL_BASE_URL: str = "https://github.com/wannaphong/thai-g2p-v3/raw/main/"
_ENCODER_FILENAME: str = "thai-g2p-v3-encoder.onnx"
_DECODER_FILENAME: str = "thai-g2p-v3-decoder.onnx"
_VOCAB_FILENAME: str = "thai-g2p-v3-vocab.json"

_ENCODER_SOURCE: str = "thai2ipa_encoder.onnx"
_DECODER_SOURCE: str = "thai2ipa_decoder.onnx"
_VOCAB_SOURCE: str = "thai2ipa_vocab.json"


def _download_file(url: str, dst: str) -> None:
    """Download a file from ``url`` to ``dst``.

    :param str url: source URL
    :param str dst: destination file path
    """
    from urllib.request import Request, urlopen

    from pythainlp import __version__

    user_agent = f"PyThaiNLP/{__version__}"
    req = Request(url, headers={"User-Agent": user_agent})
    with urlopen(req, timeout=60) as response:
        with open(dst, "wb") as f:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                f.write(chunk)


def _get_model_path(filename: str, source_basename: str) -> str:
    """Return a local path for a model file, downloading it if needed.

    :param str filename: local filename to cache the file as
    :param str source_basename: filename in the upstream GitHub repository
    :return: absolute local path to the model file
    :rtype: str
    """
    local_path: str = get_full_data_path(filename)
    if not os.path.exists(local_path):
        _logger.info("Downloading ThaiG2P v3 model file: %s ...", filename)
        _download_file(_MODEL_BASE_URL + source_basename, local_path)
    return local_path


class ThaiG2P:
    """Thai Grapheme-to-Phoneme using ONNX model (v3).

    This version uses a char-level Transformer model exported to ONNX
    for converting Thai text to International Phonetic Alphabet (IPA).

    The model files are downloaded automatically from the upstream
    repository on first use and cached in the PyThaiNLP data directory.

    For more information, see:
    https://github.com/wannaphong/thai-g2p-v3
    """

    _encoder: "InferenceSession"
    _decoder: "InferenceSession"
    _char2idx: Dict[str, int]
    _idx2char: Dict[int, str]
    _sos_idx: int
    _eos_idx: int

    def __init__(self) -> None:
        from onnxruntime import InferenceSession

        encoder_path = _get_model_path(_ENCODER_FILENAME, _ENCODER_SOURCE)
        decoder_path = _get_model_path(_DECODER_FILENAME, _DECODER_SOURCE)
        vocab_path = _get_model_path(_VOCAB_FILENAME, _VOCAB_SOURCE)

        with open(vocab_path, encoding="utf-8") as f:
            vocab: Dict[str, Dict[str, str]] = json.load(f)

        self._char2idx: Dict[str, int] = {
            k: int(v) for k, v in vocab["input_char2idx"].items()
        }
        self._idx2char: Dict[int, str] = {
            int(k): v for k, v in vocab["target_idx2char"].items()
        }
        self._sos_idx: int = self._char2idx["<SOS>"]
        self._eos_idx: int = self._char2idx["<EOS>"]

        self._encoder: "InferenceSession" = InferenceSession(
            encoder_path,
            providers=["CPUExecutionProvider"],
        )
        self._decoder: "InferenceSession" = InferenceSession(
            decoder_path,
            providers=["CPUExecutionProvider"],
        )

    def g2p(self, text: str, max_len: int = 50) -> str:
        """Convert Thai text to IPA using greedy decoding.

        :param str text: Thai text to convert
        :param int max_len: maximum output length (default: 50)
        :return: IPA representation of the input text
        :rtype: str
        """
        import numpy as np

        unk_idx: int = self._char2idx.get("<UNK>", 3)
        src: List[int] = (
            [self._sos_idx]
            + [self._char2idx.get(c, unk_idx) for c in text]
            + [self._eos_idx]
        )
        src_tensor: "NDArray[np.int64]" = np.array([src], dtype=np.int64)

        enc_outputs: list["NDArray[np.float32]"] = self._encoder.run(
            None, {"src": src_tensor}
        )
        memory: "NDArray[np.float32]" = enc_outputs[0]
        src_pad_mask: "NDArray[np.bool_]" = enc_outputs[1]

        trg_indexes: List[int] = [self._sos_idx]
        for _ in range(max_len):
            trg_tensor: "NDArray[np.int64]" = np.array(
                [trg_indexes], dtype=np.int64
            )
            dec_outputs: list["NDArray[np.float32]"] = self._decoder.run(
                None,
                {
                    "trg": trg_tensor,
                    "memory": memory,
                    "src_pad_mask": src_pad_mask,
                },
            )
            next_token_logits: "NDArray[np.float32]" = dec_outputs[0][0, -1, :]
            next_token: int = int(np.argmax(next_token_logits))
            if next_token == self._eos_idx:
                break
            trg_indexes.append(next_token)

        return "".join(self._idx2char[idx] for idx in trg_indexes[1:])


_THAI_G2P: Optional[ThaiG2P] = None


def transliterate(text: str) -> str:
    """Transliterate Thai text to IPA using ThaiG2P v3.

    :param str text: Thai text to transliterate
    :return: IPA representation of the input text
    :rtype: str
    """
    global _THAI_G2P
    if _THAI_G2P is None:
        _THAI_G2P = ThaiG2P()
    return _THAI_G2P.g2p(text)
