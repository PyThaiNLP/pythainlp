# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai Word-to-Phoneme (Thai W2P)
GitHub : https://github.com/wannaphong/Thai_W2P
"""

from typing import Union

import numpy as np
from pythainlp.corpus import download, get_corpus_path

_GRAPHEMES = list(
    "พจใงต้ืฮแาฐฒฤๅูศฅถฺฎหคสุขเึดฟำฝยลอ็ม"
    + " ณิฑชฉซทรฏฬํัฃวก่ป์ผฆบี๊ธญฌษะไ๋นโภ?"
)
_PHONEMES = list(
    "-พจใงต้ืฮแาฐฒฤูศฅถฺฎหคสุขเึดฟำฝยลอ็ม"
    + " ณิฑชฉซทรํฬฏ–ัฃวก่ปผ์ฆบี๊ธฌญะไษ๋นโภ?"
)

_MODEL_NAME = "thai_w2p"


class _Hparams:
    batch_size = 256
    enc_maxlen = 30 * 2
    dec_maxlen = 40 * 2
    num_epochs = 50 * 2
    hidden_units = 64 * 8
    emb_units = 64 * 4
    graphemes = ["<pad>", "<unk>", "</s>"] + _GRAPHEMES
    phonemes = ["<pad>", "<unk>", "<s>", "</s>"] + _PHONEMES
    lr = 0.001


hp = _Hparams()


def _load_vocab():
    g2idx = {g: idx for idx, g in enumerate(hp.graphemes)}
    idx2g = dict(enumerate(hp.graphemes))

    p2idx = {p: idx for idx, p in enumerate(hp.phonemes)}
    idx2p = dict(enumerate(hp.phonemes))
    # note that g and p mean grapheme and phoneme respectively.
    return g2idx, idx2g, p2idx, idx2p


class Thai_W2P():
    def __init__(self):
        super().__init__()
        self.graphemes = hp.graphemes
        self.phonemes = hp.phonemes
        self.g2idx, self.idx2g, self.p2idx, self.idx2p = _load_vocab()
        self.checkpoint = get_corpus_path(_MODEL_NAME, version="0.2")
        if self.checkpoint is None:
            download(_MODEL_NAME, version="0.2")
            self.checkpoint = get_corpus_path(_MODEL_NAME)
        self._load_variables()

    def _load_variables(self):
        self.variables = np.load(self.checkpoint, allow_pickle=True)
        # (29, 64). (len(graphemes), emb)
        self.enc_emb = self.variables.item().get("encoder.emb.weight")
        # (3*128, 64)
        self.enc_w_ih = self.variables.item().get("encoder.rnn.weight_ih_l0")
        # (3*128, 128)
        self.enc_w_hh = self.variables.item().get("encoder.rnn.weight_hh_l0")
        # (3*128,)
        self.enc_b_ih = self.variables.item().get("encoder.rnn.bias_ih_l0")
        # (3*128,)
        self.enc_b_hh = self.variables.item().get("encoder.rnn.bias_hh_l0")

        # (74, 64). (len(phonemes), emb)
        self.dec_emb = self.variables.item().get("decoder.emb.weight")
        # (3*128, 64)
        self.dec_w_ih = self.variables.item().get("decoder.rnn.weight_ih_l0")
        # (3*128, 128)
        self.dec_w_hh = self.variables.item().get("decoder.rnn.weight_hh_l0")
        # (3*128,)
        self.dec_b_ih = self.variables.item().get("decoder.rnn.bias_ih_l0")
        # (3*128,)
        self.dec_b_hh = self.variables.item().get("decoder.rnn.bias_hh_l0")
        # (74, 128)
        self.fc_w = self.variables.item().get("decoder.fc.weight")
        # (74,)
        self.fc_b = self.variables.item().get("decoder.fc.bias")

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def _grucell(self, x, h, w_ih, w_hh, b_ih, b_hh):
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

    def _gru(self, x, steps, w_ih, w_hh, b_ih, b_hh, h0=None) -> np.ndarray:
        if h0 is None:
            h0 = np.zeros((x.shape[0], w_hh.shape[1]), np.float32)
        h = h0  # initial hidden state

        outputs = np.zeros((x.shape[0], steps, w_hh.shape[1]), np.float32)
        for t in range(steps):
            h = self._grucell(x[:, t, :], h, w_ih, w_hh, b_ih, b_hh)  # (b, h)
            outputs[:, t, ::] = h

        return outputs

    def _encode(self, word: str) -> np.ndarray:
        chars = list(word) + ["</s>"]
        x = [self.g2idx.get(char, self.g2idx["<unk>"]) for char in chars]
        x = np.take(self.enc_emb, np.expand_dims(x, 0), axis=0)

        return x

    def _short_word(self, word: str) -> Union[str, None]:
        self.word = word
        if self.word.endswith("."):
            self.word = self.word.replace(".", "")
            self.word = "-".join([i + "อ" for i in list(self.word)])
            return self.word
        return None

    def _predict(self, word: str) -> str:
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

        preds = [self.idx2p.get(idx, "<unk>") for idx in preds]

        return preds

    def __call__(self, word: str) -> str:
        if not any(letter in word for letter in self.graphemes):
            pron = [word]
        else:  # predict for oov
            pron = self._predict(word)

        return "".join(pron)


_THAI_W2P = Thai_W2P()


def pronunciate(text: str) -> str:
    """
    Convert a Thai word to its pronunciation in Thai letters.

    Input should be one single word.

    :param str text: Thai text to be pronunciated

    :return: A string of Thai letters indicating
             how the input text should be pronounced.
    """
    return _THAI_W2P(text)
