# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Romanization of Thai words based on machine-learnt engine ("thai2rom")
"""
import random

import torch
from torch import nn
import torch.nn.functional as F
from pythainlp.corpus import get_corpus_path

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

_MODEL_NAME = "thai2rom-pytorch-attn"


class ThaiTransliterator:
    def __init__(self):
        """
        Transliteration of Thai words.

        Now supports Thai to Latin (romanization)
        """
        # get the model, download it if it's not available locally
        self.__model_filename = get_corpus_path(_MODEL_NAME)

        loader = torch.load(self.__model_filename, map_location=device)

        INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT = loader["encoder_params"]
        OUTPUT_DIM, D_EMB_DIM, D_HID_DIM, D_DROPOUT = loader["decoder_params"]

        self._maxlength = 100

        self._char_to_ix = loader["char_to_ix"]
        self._ix_to_char = loader["ix_to_char"]
        self._target_char_to_ix = loader["target_char_to_ix"]
        self._ix_to_target_char = loader["ix_to_target_char"]

        # encoder/ decoder
        # Restore the model and construct the encoder and decoder.
        self._encoder = Encoder(INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT)

        self._decoder = AttentionDecoder(
            OUTPUT_DIM, D_EMB_DIM, D_HID_DIM, D_DROPOUT
        )

        self._network = Seq2Seq(
            self._encoder,
            self._decoder,
            self._target_char_to_ix["<start>"],
            self._target_char_to_ix["<end>"],
            self._maxlength,
        ).to(device)

        self._network.load_state_dict(loader["model_state_dict"])
        self._network.eval()

    def _prepare_sequence_in(self, text: str):
        """
        Prepare input sequence for PyTorch
        """
        idxs = []
        for ch in text:
            if ch in self._char_to_ix:
                idxs.append(self._char_to_ix[ch])
            else:
                idxs.append(self._char_to_ix["<UNK>"])
        idxs.append(self._char_to_ix["<end>"])
        tensor = torch.tensor(idxs, dtype=torch.long)
        return tensor.to(device)

    def romanize(self, text: str) -> str:
        """
        :param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text
                 should be pronounced.
        """
        input_tensor = self._prepare_sequence_in(text).view(1, -1)
        input_length = torch.Tensor([len(text) + 1]).int()
        target_tensor_logits = self._network(
            input_tensor, input_length, None, 0
        )

        # Seq2seq model returns <END> as the first token,
        # As a result, target_tensor_logits.size() is torch.Size([0])
        if target_tensor_logits.size(0) == 0:
            target = ["<PAD>"]
        else:
            target_tensor = (
                torch.argmax(target_tensor_logits.squeeze(1), 1)
                .cpu()
                .detach()
                .numpy()
            )
            target = [self._ix_to_target_char[t] for t in target_tensor]

        return "".join(target)


class Encoder(nn.Module):
    def __init__(
        self, vocabulary_size, embedding_size, hidden_size, dropout=0.5
    ):
        """Constructor"""
        super().__init__()
        self.hidden_size = hidden_size
        self.character_embedding = nn.Embedding(
            vocabulary_size, embedding_size
        )
        self.rnn = nn.LSTM(
            input_size=embedding_size,
            hidden_size=hidden_size // 2,
            bidirectional=True,
            batch_first=True,
        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, sequences, sequences_lengths):

        # sequences: (batch_size, sequence_length=MAX_LENGTH)
        # sequences_lengths: (batch_size)

        batch_size = sequences.size(0)
        self.hidden = self.init_hidden(batch_size)

        sequences_lengths = torch.flip(
            torch.sort(sequences_lengths).values, dims=(0,)
        )
        index_sorted = torch.sort(-1 * sequences_lengths).indices
        index_unsort = torch.sort(index_sorted).indices  # to unsorted sequence
        sequences = sequences.index_select(0, index_sorted.to(device))

        sequences = self.character_embedding(sequences)
        sequences = self.dropout(sequences)

        sequences_packed = nn.utils.rnn.pack_padded_sequence(
            sequences, sequences_lengths.clone(), batch_first=True
        )

        sequences_output, self.hidden = self.rnn(sequences_packed, self.hidden)

        sequences_output, _ = nn.utils.rnn.pad_packed_sequence(
            sequences_output, batch_first=True
        )

        sequences_output = sequences_output.index_select(
            0, index_unsort.clone().detach()
        )
        return sequences_output, self.hidden

    def init_hidden(self, batch_size):
        h_0 = torch.zeros(
            [2, batch_size, self.hidden_size // 2], requires_grad=True
        ).to(device)
        c_0 = torch.zeros(
            [2, batch_size, self.hidden_size // 2], requires_grad=True
        ).to(device)

        return (h_0, c_0)


class Attn(nn.Module):
    def __init__(self, method, hidden_size):
        super().__init__()

        self.method = method
        self.hidden_size = hidden_size

        if self.method == "general":
            self.attn = nn.Linear(self.hidden_size, hidden_size)

        elif self.method == "concat":
            self.attn = nn.Linear(self.hidden_size * 2, hidden_size)
            self.other = nn.Parameter(torch.FloatTensor(1, hidden_size))

    def forward(self, hidden, encoder_outputs, mask):
        # Calculate energies for each encoder output
        if self.method == "dot":
            attn_energies = torch.bmm(
                encoder_outputs, hidden.transpose(1, 2)
            ).squeeze(2)
        elif self.method == "general":
            attn_energies = self.attn(
                encoder_outputs.view(-1, encoder_outputs.size(-1))
            )  # (batch_size * sequence_len,  hidden_size)
            attn_energies = torch.bmm(
                attn_energies.view(*encoder_outputs.size()),
                hidden.transpose(1, 2),
            ).squeeze(
                2
            )  # (batch_size,  sequence_len)
        elif self.method == "concat":
            attn_energies = self.attn(
                torch.cat(
                    (hidden.expand(*encoder_outputs.size()), encoder_outputs),
                    2,
                )
            )  # (batch_size, sequence_len,  hidden_size)
            attn_energies = torch.bmm(
                attn_energies,
                self.other.unsqueeze(0).expand(*hidden.size()).transpose(1, 2),
            ).squeeze(2)

        attn_energies = attn_energies.masked_fill(mask == 0, -1e10)

        # Normalize energies to weights in range 0 to 1
        return F.softmax(attn_energies, 1)


class AttentionDecoder(nn.Module):
    def __init__(
        self, vocabulary_size, embedding_size, hidden_size, dropout=0.5
    ):
        """Constructor"""
        super().__init__()
        self.vocabulary_size = vocabulary_size
        self.hidden_size = hidden_size
        self.character_embedding = nn.Embedding(
            vocabulary_size, embedding_size
        )
        self.rnn = nn.LSTM(
            input_size=embedding_size + self.hidden_size,
            hidden_size=hidden_size,
            bidirectional=False,
            batch_first=True,
        )

        self.attn = Attn(method="general", hidden_size=self.hidden_size)
        self.linear = nn.Linear(hidden_size, vocabulary_size)

        self.dropout = nn.Dropout(dropout)

    def forward(self, input_character, last_hidden, encoder_outputs, mask):
        """ "Defines the forward computation of the decoder"""

        # input_character: (batch_size, 1)
        # last_hidden: (batch_size, hidden_dim)
        # encoder_outputs: (batch_size, sequence_len, hidden_dim)
        # mask: (batch_size, sequence_len)

        hidden = last_hidden.permute(1, 0, 2)
        attn_weights = self.attn(hidden, encoder_outputs, mask)

        context_vector = attn_weights.unsqueeze(1).bmm(encoder_outputs)
        context_vector = torch.sum(context_vector, dim=1)
        context_vector = context_vector.unsqueeze(1)

        embedded = self.character_embedding(input_character)
        embedded = self.dropout(embedded)

        rnn_input = torch.cat((context_vector, embedded), -1)

        output, hidden = self.rnn(rnn_input)
        output = output.view(-1, output.size(2))

        x = self.linear(output)

        return x, hidden[0], attn_weights


class Seq2Seq(nn.Module):
    def __init__(
        self,
        encoder,
        decoder,
        target_start_token,
        target_end_token,
        max_length,
    ):
        super().__init__()

        self.encoder = encoder
        self.decoder = decoder
        self.pad_idx = 0
        self.target_start_token = target_start_token
        self.target_end_token = target_end_token
        self.max_length = max_length

        assert encoder.hidden_size == decoder.hidden_size

    def create_mask(self, source_seq):
        mask = source_seq != self.pad_idx
        return mask

    def forward(
        self, source_seq, source_seq_len, target_seq, teacher_forcing_ratio=0.5
    ):

        # source_seq: (batch_size, MAX_LENGTH)
        # source_seq_len: (batch_size, 1)
        # target_seq: (batch_size, MAX_LENGTH)

        batch_size = source_seq.size(0)
        start_token = self.target_start_token
        end_token = self.target_end_token
        max_len = self.max_length
        target_vocab_size = self.decoder.vocabulary_size

        outputs = torch.zeros(max_len, batch_size, target_vocab_size).to(
            device
        )

        if target_seq is None:
            assert teacher_forcing_ratio == 0, "Must be zero during inference"
            inference = True
        else:
            inference = False

        encoder_outputs, encoder_hidden = self.encoder(
            source_seq, source_seq_len
        )

        decoder_input = (
            torch.tensor([[start_token] * batch_size])
            .view(batch_size, 1)
            .to(device)
        )

        encoder_hidden_h_t = torch.cat(
            [encoder_hidden[0][0], encoder_hidden[0][1]], dim=1
        ).unsqueeze(dim=0)
        decoder_hidden = encoder_hidden_h_t

        max_source_len = encoder_outputs.size(1)
        mask = self.create_mask(source_seq[:, 0:max_source_len])

        for di in range(max_len):
            decoder_output, decoder_hidden, _ = self.decoder(
                decoder_input, decoder_hidden, encoder_outputs, mask
            )

            _, topi = decoder_output.topk(1)
            outputs[di] = decoder_output.to(device)

            teacher_force = random.random() < teacher_forcing_ratio

            decoder_input = (
                target_seq[:, di].reshape(batch_size, 1)
                if teacher_force
                else topi.detach()
            )

            decoder_input = topi.detach()

            if inference and decoder_input == end_token:
                return outputs[:di]

        return outputs


_THAI_TO_ROM = ThaiTransliterator()


def romanize(text: str) -> str:
    return _THAI_TO_ROM.romanize(text)
