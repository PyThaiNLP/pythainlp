# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai Grapheme-to-Phoneme (Thai G2P) v3

GitHub: https://github.com/wannaphong/thai-g2p-v3
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Dict, List, Optional

from pythainlp.corpus import get_corpus_path

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray
    from onnxruntime import InferenceSession

_MODEL_ENCODER_NAME: str = "thaig2p_v3_encoder_onnx"
_MODEL_DECODER_NAME: str = "thaig2p_v3_decoder_onnx"
_MODEL_VOCAB_NAME: str = "thaig2p_v3_vocab"


class ThaiG2P:
    """Thai Grapheme-to-Phoneme using ONNX model (v3).

    This version uses a char-level Transformer model exported to ONNX
    for converting Thai text to International Phonetic Alphabet (IPA).

    Model files are bundled with PyThaiNLP in the corpus directory.

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

        encoder_path = get_corpus_path(_MODEL_ENCODER_NAME)
        decoder_path = get_corpus_path(_MODEL_DECODER_NAME)
        vocab_path = get_corpus_path(_MODEL_VOCAB_NAME)

        missing = [
            n
            for n, v in (
                (_MODEL_ENCODER_NAME, encoder_path),
                (_MODEL_DECODER_NAME, decoder_path),
                (_MODEL_VOCAB_NAME, vocab_path),
            )
            if not v
        ]
        if missing:
            raise FileNotFoundError(
                f"corpus-not-found names={missing!r}\n"
                f"  Corpus file(s) not found: {', '.join(missing)}."
            )

        with open(str(vocab_path), encoding="utf-8") as f:
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
            str(encoder_path),
            providers=["CPUExecutionProvider"],
        )
        self._decoder: "InferenceSession" = InferenceSession(
            str(decoder_path),
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
