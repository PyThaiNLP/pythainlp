# -*- coding: utf-8 -*-
"""
Thai Word-to-Phoneme
GitHub : https://github.com/wannaphong/Thai_G2P
"""

import numpy as np
import codecs
import os
import re
from pythainlp.corpus import download, get_corpus_path


class Hparams:
    batch_size = 256
    enc_maxlen = 30*2
    dec_maxlen = 40*2
    num_epochs = 50*2
    hidden_units = 64*8
    emb_units = 64*4
    graphemes = ["<pad>", "<unk>", "</s>"] + list('พจใงต้ืฮแาฐฒฤๅูศฅถฺฎหคสุขเึดฟำฝยลอ็ม ณิฑชฉซทรฏฬํัฃวก่ป์ผฆบี๊ธญฌษะไ๋นโภ?')
    phonemes = ["<pad>", "<unk>", "<s>", "</s>"] + list('-พจใงต้ืฮแาฐฒฤูศฅถฺฎหคสุขเึดฟำฝยลอ็ม ณิฑชฉซทรํฬฏ–ัฃวก่ปผ์ฆบี๊ธฌญะไษ๋นโภ?')
    lr = 0.001


hp = Hparams()


def load_vocab():
    g2idx = {g: idx for idx, g in enumerate(hp.graphemes)}
    idx2g = {idx: g for idx, g in enumerate(hp.graphemes)}

    p2idx = {p: idx for idx, p in enumerate(hp.phonemes)}
    idx2p = {idx: p for idx, p in enumerate(hp.phonemes)}
    return g2idx, idx2g, p2idx, idx2p  # note that g and p mean grapheme and phoneme, respectively.


class G2P(object):
    def __init__(self):
        super().__init__()
        self.graphemes = hp.graphemes
        self.phonemes = hp.phonemes
        self.g2idx, self.idx2g, self.p2idx, self.idx2p = load_vocab()
        self.checkpoint = get_corpus_path('thai_w2p')
        if self.checkpoint is None:
            download('thai_w2p')
            self.checkpoint = get_corpus_path('thai_w2p')
        self.load_variables()

    def load_variables(self):
        self.variables = np.load(self.checkpoint, allow_pickle=True)
        self.enc_emb = self.variables.item().get("encoder.emb.weight")  # (29, 64). (len(graphemes), emb)
        self.enc_w_ih = self.variables.item().get("encoder.rnn.weight_ih_l0")  # (3*128, 64)
        self.enc_w_hh = self.variables.item().get("encoder.rnn.weight_hh_l0")  # (3*128, 128)
        self.enc_b_ih = self.variables.item().get("encoder.rnn.bias_ih_l0")  # (3*128,)
        self.enc_b_hh = self.variables.item().get("encoder.rnn.bias_hh_l0")  # (3*128,)

        self.dec_emb = self.variables.item().get("decoder.emb.weight")  # (74, 64). (len(phonemes), emb)
        self.dec_w_ih = self.variables.item().get("decoder.rnn.weight_ih_l0")  # (3*128, 64)
        self.dec_w_hh = self.variables.item().get("decoder.rnn.weight_hh_l0")  # (3*128, 128)
        self.dec_b_ih = self.variables.item().get("decoder.rnn.bias_ih_l0")  # (3*128,)
        self.dec_b_hh = self.variables.item().get("decoder.rnn.bias_hh_l0")  # (3*128,)
        self.fc_w = self.variables.item().get("decoder.fc.weight")  # (74, 128)
        self.fc_b = self.variables.item().get("decoder.fc.bias")  # (74,)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def grucell(self, x, h, w_ih, w_hh, b_ih, b_hh):
        rzn_ih = np.matmul(x, w_ih.T) + b_ih
        rzn_hh = np.matmul(h, w_hh.T) + b_hh

        rz_ih, n_ih = rzn_ih[:, :rzn_ih.shape[-1] * 2 // 3], rzn_ih[:, rzn_ih.shape[-1] * 2 // 3:]
        rz_hh, n_hh = rzn_hh[:, :rzn_hh.shape[-1] * 2 // 3], rzn_hh[:, rzn_hh.shape[-1] * 2 // 3:]

        rz = self.sigmoid(rz_ih + rz_hh)
        r, z = np.split(rz, 2, -1)

        n = np.tanh(n_ih + r * n_hh)
        h = (1 - z) * n + z * h

        return h

    def gru(self, x, steps, w_ih, w_hh, b_ih, b_hh, h0=None):
        if h0 is None:
            h0 = np.zeros((x.shape[0], w_hh.shape[1]), np.float32)
        h = h0  # initial hidden state
        outputs = np.zeros((x.shape[0], steps, w_hh.shape[1]), np.float32)
        for t in range(steps):
            h = self.grucell(x[:, t, :], h, w_ih, w_hh, b_ih, b_hh)  # (b, h)
            outputs[:, t, ::] = h
        return outputs

    def encode(self, word: str):
        chars = list(word) + ["</s>"]
        x = [self.g2idx.get(char, self.g2idx["<unk>"]) for char in chars]
        x = np.take(self.enc_emb, np.expand_dims(x, 0), axis=0)

        return x

    def predict(self, word: str):
        # encoder
        enc = self.encode(word)
        enc = self.gru(enc, len(word) + 1, self.enc_w_ih, self.enc_w_hh,
                       self.enc_b_ih, self.enc_b_hh, h0=np.zeros((1, self.enc_w_hh.shape[-1]), np.float32))
        last_hidden = enc[:, -1, :]

        # decoder
        dec = np.take(self.dec_emb, [2], axis=0)  # 2: <s>
        h = last_hidden

        preds = []
        for i in range(20):
            h = self.grucell(dec, h, self.dec_w_ih, self.dec_w_hh, self.dec_b_ih, self.dec_b_hh)  # (b, h)
            logits = np.matmul(h, self.fc_w.T) + self.fc_b
            pred = logits.argmax()
            if pred == 3:
                break
            preds.append(pred)
            dec = np.take(self.dec_emb, [pred], axis=0)

        preds = [self.idx2p.get(idx, "<unk>") for idx in preds]
        return preds

    def __call__(self, text: str):
        # tokenization
        word = text
        if not any(letter in word for letter in self.graphemes):
            pron = [word]
        else:  # predict for oov
            pron = self.predict(word)

        return ''.join(pron)


def transliterate(text: str) -> str:
    _g2p = G2P()
    return _g2p(text)
