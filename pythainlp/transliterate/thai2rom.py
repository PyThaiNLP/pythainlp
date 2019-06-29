# -*- coding: utf-8 -*-
"""
Romanization of Thai words based on machine-learnt engine ("thai2rom")
"""
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from pythainlp.corpus import download, get_corpus_path

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class ThaiTransliterator:
    def __init__(self):
        """
        Transliteration of Thai words
        Now supports Thai to Latin (romanization)
        """
        # Download the model, if it's not on your machine.
        self.__filemodel = get_corpus_path("thai2rom-pytorch")
        if not self.__filemodel:
            download("thai2rom-pytorch")
            self.__filemodel = get_corpus_path("thai2rom-pytorch")
        loader = torch.load(self.__filemodel)
        self._n_h = 64  # hidden dimensions for encoder
        self._n_s = 64  # hidden dimensions for decoder
        self._emb_dim = 64  # character embedding size
        self._maxlength = 100
        self._char_to_ix = loader['char_to_ix']
        self._ix_to_char = loader['ix_to_char']
        self._target_char_to_ix = loader['target_char_to_ix']
        self._ix_to_target_char = loader['ix_to_target_char']
        # encoder/ decoder
        # Restore the model and construct the encoder and decoder.
        self._encoder = Encoder(len(self._char_to_ix),
                                self._n_h, self._emb_dim).to(device)
        self._encoder.load_state_dict(loader['encoder_state_dict'])
        self._decoder = OneStepDecoder(
            len(self._target_char_to_ix), self._n_s, self._emb_dim).to(device)
        self._decoder.load_state_dict(loader['decoder_state_dict'])

    def _prepare_sequence_in(self, input_text):
        """
        Prepare input sequence for PyTorch
        """
        idxs = []
        for w in input_text:
            if w in self._char_to_ix:
                idxs.append(self._char_to_ix[w])
            else:
                idxs.append(self._char_to_ix["<UNK>"])
        idxs.append(self._target_char_to_ix["<end>"])
        tensor = torch.tensor(idxs, dtype=torch.long)
        return tensor.to(device)

    def romanize(self, input_text):
        """
        :param str input_text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text should be pronounced.
        """
        input_tensor = self._prepare_sequence_in(input_text)
        input_length = input_tensor.size(0)
        encoder_outputs, encoder_hidden = self._encoder(input_tensor)
        decoder_input = torch.tensor(
            [self._target_char_to_ix["<start>"]], device=device)
        decoder_hidden = (
            encoder_hidden[0].reshape(
                1, 1, self._encoder.hidden_dim), encoder_hidden[1].reshape(
                1, 1, self._encoder.hidden_dim))

        decoded_seq = []  # output

        for di in range(self._maxlength):
            decoder_output, decoder_hidden, _ = self._decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == self._target_char_to_ix["<end>"]:
                decoded_seq.append('<end>')
                break
            else:
                decoded_seq.append(self._ix_to_target_char[topi.item()])

            decoder_input = topi.squeeze().detach()

        return "".join(decoded_seq[:-1])


class Encoder(nn.Module):
    def __init__(self, vocab_size, hidden_dim, emb_dim):
        super(Encoder, self).__init__()
        self.hidden_dim = hidden_dim
        self.char_emb = nn.Embedding(vocab_size, emb_dim)
        self.lstm = nn.LSTM(emb_dim, self.hidden_dim // 2, bidirectional=True)

    def forward(self, input_seq):
        self.hidden = self.init_hidden()
        embedded = self.char_emb(input_seq)
        output, self.hidden = self.lstm(
            embedded.view(len(embedded), 1, -1), self.hidden)
        return output, self.hidden

    def init_hidden(self):
        # The axes semantics are (num_layers, minibatch_size, hidden_dim)
        return (
            torch.zeros(
                2,
                1,
                self.hidden_dim // 2,
                requires_grad=True).to(device),
            torch.zeros(
                2,
                1,
                self.hidden_dim // 2,
                requires_grad=True).to(device))


class OneStepDecoder(nn.Module):
    def __init__(self, vocab_size, hidden_dim, emb_dim):
        super(OneStepDecoder, self).__init__()
        self.hidden_dim = hidden_dim
        self.char_emb = nn.Embedding(vocab_size, emb_dim)
        self.lstm = nn.LSTM(emb_dim, hidden_dim)
        self.out = nn.Linear(hidden_dim, vocab_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input_step, hidden, encoder_outputs):

        embedded = self.char_emb(input_step).view(1, 1, -1)
        output = embedded
        output = F.relu(output)
        output, hidden = self.lstm(output, hidden)
        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, []  # this empty list should be replaced with decoder attn score

    def init_hidden(self):
        # The axes semantics are (num_layers, minibatch_size, hidden_dim)
        return (
            torch.zeros(
                1,
                1,
                self.hidden_dim,
                requires_grad=True).to(device),
            torch.zeros(
                1,
                1,
                self.hidden_dim,
                requires_grad=True).to(device))


_THAI_TO_ROM = ThaiTransliterator()


def romanize(text: str) -> str:
    return _THAI_TO_ROM.romanize(text)
