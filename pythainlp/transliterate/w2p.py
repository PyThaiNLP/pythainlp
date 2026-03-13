# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai Word-to-Phoneme (Thai W2P)
GitHub : https://github.com/wannaphong/Thai_W2P
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pythainlp.corpus import get_corpus_path

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray

_GRAPHEMES: list[str] = list(
    "พจใงต้ืฮแาฐฒฤๅูศฅถฺฎหคสุขเึดฟำฝยลอ็ม" + " ณิฑชฉซทรฏฬํัฃวก่ป์ผฆบี๊ธญฌษะไ๋นโภ?"
)
_PHONEMES: list[str] = list(
    "-พจใงต้ืฮแาฐฒฤูศฅถฺฎหคสุขเึดฟำฝยลอ็ม" + " ณิฑชฉซทรํฬฏ–ัฃวก่ปผ์ฆบี๊ธฌญะไษ๋นโภ?"
)

_MODEL_NAME: str = "thai_w2p"


class _Hparams:
    batch_size: int = 256
    enc_maxlen: int = 30 * 2
    dec_maxlen: int = 40 * 2
    num_epochs: int = 50 * 2
    hidden_units: int = 64 * 8
    emb_units: int = 64 * 4
    graphemes: list[str] = ["<pad>", "<unk>", "</s>"] + _GRAPHEMES
    phonemes: list[str] = ["<pad>", "<unk>", "<s>", "</s>"] + _PHONEMES
    lr: float = 0.001


hp: _Hparams = _Hparams()


def _load_vocab() -> tuple[
    dict[str, int], dict[int, str], dict[str, int], dict[int, str]
]:
    g2idx = {g: idx for idx, g in enumerate(hp.graphemes)}
    idx2g = dict(enumerate(hp.graphemes))

    p2idx = {p: idx for idx, p in enumerate(hp.phonemes)}
    idx2p = dict(enumerate(hp.phonemes))
    # note that g and p mean grapheme and phoneme respectively.
    return g2idx, idx2g, p2idx, idx2p


class Thai_W2P:
    graphemes: list[str]
    phonemes: list[str]
    g2idx: dict[str, int]
    idx2g: dict[int, str]
    p2idx: dict[str, int]
    idx2p: dict[int, str]
    checkpoint: Optional[str]
    enc_emb: "NDArray"
    enc_w_ih: "NDArray"
    enc_w_hh: "NDArray"
    enc_b_ih: "NDArray"
    enc_b_hh: "NDArray"
    dec_emb: "NDArray"
    dec_w_ih: "NDArray"
    dec_w_hh: "NDArray"
    dec_b_ih: "NDArray"
    dec_b_hh: "NDArray"
    fc_w: "NDArray"
    fc_b: "NDArray"
    word: str

    def __init__(self) -> None:
        super().__init__()
        self.graphemes: list[str] = hp.graphemes
        self.phonemes: list[str] = hp.phonemes
        self.g2idx: dict[str, int]
        self.idx2g: dict[int, str]
        self.p2idx: dict[str, int]
        self.idx2p: dict[int, str]
        self.g2idx, self.idx2g, self.p2idx, self.idx2p = _load_vocab()
        self.checkpoint: Optional[str] = get_corpus_path(
            _MODEL_NAME, version="0.2"
        )
        if not self.checkpoint:
            raise FileNotFoundError(
                f"corpus-not-found name={_MODEL_NAME!r}\n"
                f"  Corpus '{_MODEL_NAME}' not found.\n"
                f"    Python: pythainlp.corpus.download('{_MODEL_NAME}', version='0.2')\n"
                f"    CLI:    thainlp data get {_MODEL_NAME}"
            )
        self._load_variables()

    def _load_variables(self) -> None:
        import numpy as np

        if self.checkpoint is None:
            raise RuntimeError("checkpoint path is not set")
        variables: "np.lib.npyio.NpzFile" = np.load(
            self.checkpoint, allow_pickle=False
        )
        # (29, 64). (len(graphemes), emb)
        self.enc_emb: "NDArray" = variables["encoder.emb.weight"]
        # (3*128, 64)
        self.enc_w_ih: "NDArray" = variables["encoder.rnn.weight_ih_l0"]
        # (3*128, 128)
        self.enc_w_hh: "NDArray" = variables["encoder.rnn.weight_hh_l0"]
        # (3*128,)
        self.enc_b_ih: "NDArray" = variables["encoder.rnn.bias_ih_l0"]
        # (3*128,)
        self.enc_b_hh: "NDArray" = variables["encoder.rnn.bias_hh_l0"]
        # (74, 64). (len(phonemes), emb)
        self.dec_emb: "NDArray" = variables["decoder.emb.weight"]
        # (3*128, 64)
        self.dec_w_ih: "NDArray" = variables["decoder.rnn.weight_ih_l0"]
        # (3*128, 128)
        self.dec_w_hh: "NDArray" = variables["decoder.rnn.weight_hh_l0"]
        # (3*128,)
        self.dec_b_ih: "NDArray" = variables["decoder.rnn.bias_ih_l0"]
        # (3*128,)
        self.dec_b_hh: "NDArray" = variables["decoder.rnn.bias_hh_l0"]
        # (74, 128)
        self.fc_w: "NDArray" = variables["decoder.fc.weight"]
        # (74,)
        self.fc_b: "NDArray" = variables["decoder.fc.bias"]

    def _sigmoid(self, x: "np.ndarray") -> "np.ndarray":
        import numpy as np

        return 1 / (1 + np.exp(-x))

    def _grucell(
        self,
        x: "np.ndarray",
        h: "np.ndarray",
        w_ih: "np.ndarray",
        w_hh: "np.ndarray",
        b_ih: "np.ndarray",
        b_hh: "np.ndarray",
    ) -> "np.ndarray":
        import numpy as np

        rzn_ih = np.matmul(x, w_ih.T) + b_ih
        rzn_hh = np.matmul(h, w_hh.T) + b_hh

        rz_ih, n_ih = (
            rzn_ih[:, : rzn_ih.shape[-1] * 2 // 3],
            rzn_ih[:, rzn_ih.shape[-1] * 2 // 3 :],
        )
        rz_hh, n_hh = (
            rzn_hh[:, : rzn_hh.shape[-1] * 2 // 3],
            rzn_hh[:, rzn_hh.shape[-1] * 2 // 3 :],
        )

        rz = self._sigmoid(rz_ih + rz_hh)
        r, z = np.split(rz, 2, -1)

        n = np.tanh(n_ih + r * n_hh)
        h = (1 - z) * n + z * h

        return h

    def _gru(
        self,
        x: "np.ndarray",
        steps: int,
        w_ih: "np.ndarray",
        w_hh: "np.ndarray",
        b_ih: "np.ndarray",
        b_hh: "np.ndarray",
        h0: Optional["np.ndarray"] = None,
    ) -> "np.ndarray":
        import numpy as np

        if h0 is None:
            h0 = np.zeros((x.shape[0], w_hh.shape[1]), np.float32)
        h = h0  # initial hidden state

        outputs = np.zeros((x.shape[0], steps, w_hh.shape[1]), np.float32)
        for t in range(steps):
            h = self._grucell(x[:, t, :], h, w_ih, w_hh, b_ih, b_hh)  # (b, h)
            outputs[:, t, ::] = h

        return outputs

    def _encode(self, word: str) -> "np.ndarray":
        import numpy as np

        chars = list(word) + ["</s>"]
        x = [self.g2idx.get(char, self.g2idx["<unk>"]) for char in chars]
        x = np.take(self.enc_emb, np.expand_dims(x, 0), axis=0)

        return x

    def _short_word(self, word: str) -> Optional[str]:
        self.word: str = word
        if self.word.endswith("."):
            self.word = self.word.replace(".", "")
            self.word = "-".join([i + "อ" for i in list(self.word)])
            return self.word
        return None

    def _predict(self, word: str) -> str:
        import numpy as np

        short_word = self._short_word(word)
        if short_word is not None:
            return short_word

        # encoder
        enc = self._encode(word)
        enc = self._gru(
            enc,
            len(word) + 1,
            self.enc_w_ih,
            self.enc_w_hh,
            self.enc_b_ih,
            self.enc_b_hh,
            h0=np.zeros((1, self.enc_w_hh.shape[-1]), np.float32),
        )
        last_hidden = enc[:, -1, :]

        # decoder
        dec = np.take(self.dec_emb, [2], axis=0)  # 2: <s>
        h = last_hidden

        preds = []
        for _ in range(20):
            h = self._grucell(
                dec,
                h,
                self.dec_w_ih,
                self.dec_w_hh,
                self.dec_b_ih,
                self.dec_b_hh,
            )  # (b, h)
            logits = np.matmul(h, self.fc_w.T) + self.fc_b
            pred = logits.argmax()
            if pred == 3:
                break
            preds.append(pred)
            dec = np.take(self.dec_emb, [pred], axis=0)

        preds_str = [self.idx2p.get(idx, "<unk>") for idx in preds]

        return "".join(preds_str)

    def __call__(self, word: str) -> str:
        if not any(letter in word for letter in self.graphemes):
            pron_result = word
        else:  # predict for oov
            pron_result = self._predict(word)

        return pron_result


_THAI_W2P: "Thai_W2P" = Thai_W2P()


def pronunciate(text: str) -> str:
    """Convert a Thai word to its pronunciation in Thai letters.

    Input should be one single word.

    :param str text: Thai text to be pronunciated

    :return: A string of Thai letters indicating
             how the input text should be pronounced.
    """
    return _THAI_W2P(text)
