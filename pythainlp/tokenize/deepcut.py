# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""DeepCut Thai word segmentation using ONNX runtime.

DeepCut is a Thai word segmentation library using 1D Convolution Neural
Network. This module provides ONNX-based inference, removing the need for
TensorFlow.

The ONNX model is ported from the original DeepCut TensorFlow model,
available from the LEKCut project.

:See Also:
    * `DeepCut GitHub <https://github.com/rkcosmos/deepcut>`_
    * `LEKCut GitHub <https://github.com/PyThaiNLP/LEKCut>`_

:References:
    Rakpong Kittinaradorn, Titipat Achakulvisut, Korakot Chaovavanich,
    Kittinan Srithaworn, Pattarawat Chormai, Chanwit Kaewkasi,
    Tulakan Ruangrong, Krichkorn Oparad.
    (2019, September 23). DeepCut: A Thai word tokenization library using
    Deep Neural Network. Zenodo. https://doi.org/10.5281/zenodo.3457707
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

import numpy as np
from onnxruntime import InferenceSession

from pythainlp.corpus import get_corpus_path
from pythainlp.util import Trie

if TYPE_CHECKING:
    from numpy.typing import NDArray

_MODEL_NAME: str = "deepcut_onnx"
_N_PAD: int = 21
_THRESHOLD: float = 0.5

# Character type mapping from the original DeepCut model
_CHAR_TYPE: dict[str, str] = {
    "กขฃคฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมยรลวศษสฬอ": "c",
    "ฅฉผฟฌหฮ": "n",
    "ะาำิีืึุู": "v",
    "เแโใไ": "w",
    "่้๊๋": "t",
    "์ๆฯ.": "s",
    "0123456789๑๒๓๔๕๖๗๘๙": "d",
    '"': "q",
    "'": "q",
    "\u2018": "q",
    "\u2019": "q",
    " ": "p",
    "abcdefghijklmnopqrstuvwxyz": "s_e",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "b_e",
}

_CHAR_TYPE_FLAT: dict[str, str] = {}
for _ks, _ct in _CHAR_TYPE.items():
    for _k in _ks:
        _CHAR_TYPE_FLAT[_k] = _ct

_CHARS: list[str] = [
    "\n", " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+",
    ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8",
    "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E",
    "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
    "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "other", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
    "z", "}", "~", "ก", "ข", "ฃ", "ค", "ฅ", "ฆ", "ง", "จ", "ฉ", "ช",
    "ซ", "ฌ", "ญ", "ฎ", "ฏ", "ฐ", "ฑ", "ฒ", "ณ", "ด", "ต", "ถ", "ท",
    "ธ", "น", "บ", "ป", "ผ", "ฝ", "พ", "ฟ", "ภ", "ม", "ย", "ร", "ฤ",
    "ล", "ว", "ศ", "ษ", "ส", "ห", "ฬ", "อ", "ฮ", "ฯ", "ะ", "ั", "า",
    "ำ", "ิ", "ี", "ึ", "ื", "ุ", "ู", "ฺ", "เ", "แ", "โ", "ใ", "ไ",
    "ๅ", "ๆ", "็", "่", "้", "๊", "๋", "์", "ํ", "๐", "๑", "๒", "๓",
    "๔", "๕", "๖", "๗", "๘", "๙", "\u2018", "\u2019", "\ufeff",
]
_CHARS_MAP: dict[str, int] = {v: k for k, v in enumerate(_CHARS)}

_CHAR_TYPES: list[str] = [
    "b_e", "c", "d", "n", "o", "p", "q", "s", "s_e", "t", "v", "w",
]
_CHAR_TYPES_MAP: dict[str, int] = {v: k for k, v in enumerate(_CHAR_TYPES)}

# Default index for unknown characters and types
_OTHER_CHAR_INDEX: int = _CHARS_MAP.get("other", 80)
_OTHER_TYPE_INDEX: int = _CHAR_TYPES_MAP.get("o", 4)

_session: Optional[InferenceSession] = None


def _get_session() -> InferenceSession:
    """Return a cached ONNX inference session, loading it on first call."""
    global _session
    if _session is None:
        model_path = get_corpus_path(_MODEL_NAME)
        if not model_path:
            raise FileNotFoundError(
                f"corpus-not-found name={_MODEL_NAME!r}\n"
                "  DeepCut ONNX model file not found in the package.\n"
                "  Try reinstalling PyThaiNLP:\n"
                "    pip install --force-reinstall pythainlp"
            )
        _session = InferenceSession(model_path)
    return _session


def _create_feature_array(
    text: str, n_pad: int = _N_PAD
) -> tuple["NDArray[np.float32]", "NDArray[np.float32]"]:
    """Create character and type feature arrays for ONNX model input.

    :param str text: input text
    :param int n_pad: window size for padding (default: 21)
    :return: character and type feature arrays of shape (n, n_pad)
    :rtype: tuple[numpy.ndarray, numpy.ndarray]
    """
    n = len(text)
    n_pad_2 = (n_pad - 1) // 2
    text_pad = [" "] * n_pad_2 + list(text) + [" "] * n_pad_2
    x_char: list[list[int]] = []
    x_type: list[list[int]] = []
    for i in range(n_pad_2, n_pad_2 + n):
        char_list = (
            text_pad[i + 1 : i + n_pad_2 + 1]
            + list(reversed(text_pad[i - n_pad_2 : i]))
            + [text_pad[i]]
        )
        x_char.append([_CHARS_MAP.get(c, _OTHER_CHAR_INDEX) for c in char_list])
        x_type.append(
            [
                _CHAR_TYPES_MAP.get(_CHAR_TYPE_FLAT.get(c, "o"), _OTHER_TYPE_INDEX)
                for c in char_list
            ]
        )
    return (
        np.array(x_char, dtype=np.float32),
        np.array(x_type, dtype=np.float32),
    )


def segment(
    text: str,
    custom_dict: Union[Trie, list[str], str, None] = None,
) -> list[str]:
    """Segment Thai text using the DeepCut ONNX model.

    :param str text: text to segment
    :param custom_dict: ignored; kept for API compatibility only
    :type custom_dict: Union[pythainlp.util.Trie, list[str], str, None]
    :return: list of word tokens
    :rtype: list[str]

    :Example:
    ::

        from pythainlp.tokenize import deepcut

        deepcut.segment("ทดสอบตัดคำ")
        # output: ['ทดสอบ', 'ตัด', 'คำ']
    """
    if not text or not isinstance(text, str):
        return []

    session = _get_session()
    x_char, x_type = _create_feature_array(text)
    outputs = session.run(None, {"input_1": x_char, "input_2": x_type})
    y_predict = (outputs[0].ravel() > _THRESHOLD).astype(int)
    word_end = y_predict[1:].tolist() + [1]

    tokens: list[str] = []
    word = ""
    for char, is_end in zip(text, word_end):
        word += char
        if is_end:
            tokens.append(word)
            word = ""
    return tokens
