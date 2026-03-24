# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai Grapheme-to-Phoneme (Thai G2P)
GitHub : https://github.com/wannaphong/thai-g2p
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any, Optional, Union

import torch
import torch.nn.functional as F
from torch import nn

from pythainlp.corpus import get_corpus_path

if TYPE_CHECKING:
    from numpy.typing import NDArray

device: torch.device = torch.device(
    "cuda:0" if torch.cuda.is_available() else "cpu"
)

_MODEL_NAME: str = "thai-g2p"


class ThaiG2P:
    """
    Thai Grapheme-to-Phoneme using PyTorch-based model (v1).

    This is the original Thai G2P model that converts Thai text to
    International Phonetic Alphabet (IPA) representation using a custom
    PyTorch neural network architecture.

    For more information, see:
    https://github.com/wannaphong/thai-g2p
    """

    __model_filename: str
    _maxlength: int
    _char_to_ix: dict[str, int]
    _ix_to_char: dict[int, str]
    _target_char_to_ix: dict[str, int]
    _ix_to_target_char: dict[int, str]
    _encoder: "Encoder"
    _decoder: "AttentionDecoder"
    _network: "Seq2Seq"

    def __init__(self) -> None:
        self.__model_filename: str = get_corpus_path(_MODEL_NAME)  # type: ignore[assignment]
        if not self.__model_filename:
            raise FileNotFoundError(
                f"corpus-not-found name={_MODEL_NAME!r}\n"
                f"  Corpus '{_MODEL_NAME}' not found.\n"
                f"    Python: pythainlp.corpus.download('{_MODEL_NAME}')\n"
                f"    CLI:    thainlp data get {_MODEL_NAME}"
            )

        loader = torch.load(self.__model_filename, map_location=device)

        INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT = loader["encoder_params"]
        OUTPUT_DIM, D_EMB_DIM, D_HID_DIM, D_DROPOUT = loader["decoder_params"]

        self._maxlength: int = 100

        self._char_to_ix: dict[str, int] = loader["char_to_ix"]
        self._ix_to_char: dict[int, str] = loader["ix_to_char"]
        self._target_char_to_ix: dict[str, int] = loader["target_char_to_ix"]
        self._ix_to_target_char: dict[int, str] = loader["ix_to_target_char"]

        # encoder/ decoder
        # Restore the model and construct the encoder and decoder.
        self._encoder: "Encoder" = Encoder(
            INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT
        )

        self._decoder: "AttentionDecoder" = AttentionDecoder(
            OUTPUT_DIM, D_EMB_DIM, D_HID_DIM, D_DROPOUT
        )

        self._network: "Seq2Seq" = Seq2Seq(
            self._encoder,
            self._decoder,
            self._target_char_to_ix["<start>"],
            self._target_char_to_ix["<end>"],
            self._maxlength,
        ).to(device)

        self._network.load_state_dict(loader["model_state_dict"])
        self._network.eval()

    def _prepare_sequence_in(self, text: str) -> torch.Tensor:
        """Prepare input sequence for PyTorch."""
        idxs = []
        for ch in text:
            if ch in self._char_to_ix:
                idxs.append(self._char_to_ix[ch])
            else:
                idxs.append(self._char_to_ix["<UNK>"])
        idxs.append(self._char_to_ix["<end>"])
        tensor = torch.tensor(idxs, dtype=torch.long)
        return tensor.to(device)

    def g2p(self, text: str) -> str:
        """:param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text
                 should be pronounced.
        """
        input_tensor = self._prepare_sequence_in(text).view(1, -1)
        input_length = [len(text) + 1]

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


class Encoder(nn.Module):  # type: ignore[misc]
    hidden_size: int
    character_embedding: nn.Embedding
    rnn: nn.LSTM
    dropout: nn.Dropout
    hidden: tuple[torch.Tensor, torch.Tensor]

    def __init__(
        self,
        vocabulary_size: int,
        embedding_size: int,
        hidden_size: int,
        dropout: float = 0.5,
    ) -> None:
        """Constructor"""
        super().__init__()
        self.hidden_size: int = hidden_size
        self.character_embedding: nn.Embedding = nn.Embedding(
            vocabulary_size, embedding_size
        )
        self.rnn: nn.LSTM = nn.LSTM(
            input_size=embedding_size,
            hidden_size=hidden_size // 2,
            bidirectional=True,
            batch_first=True,
        )

        self.dropout: nn.Dropout = nn.Dropout(dropout)

    def forward(
        self,
        sequences: torch.Tensor,
        sequences_lengths: Union[NDArray[Any], list[int]],
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        # sequences: (batch_size, sequence_length=MAX_LENGTH)
        # sequences_lengths: (batch_size)
        import numpy as np

        batch_size = sequences.size(0)
        self.hidden: tuple[torch.Tensor, torch.Tensor] = self.init_hidden(
            batch_size
        )

        sequences_lengths = np.sort(sequences_lengths)[::-1]
        index_sorted = np.argsort(
            -sequences_lengths
        )  # use negation in sort in descending order
        index_unsort = np.argsort(index_sorted)  # to unsorted sequence

        index_sorted = torch.from_numpy(index_sorted)
        sequences = sequences.index_select(0, index_sorted.to(device))

        sequences = self.character_embedding(sequences)
        sequences = self.dropout(sequences)

        sequences_packed = nn.utils.rnn.pack_padded_sequence(
            sequences, sequences_lengths.copy(), batch_first=True
        )

        sequences_output, self.hidden = self.rnn(sequences_packed, self.hidden)

        sequences_output, _ = nn.utils.rnn.pad_packed_sequence(
            sequences_output, batch_first=True
        )

        index_unsort = torch.from_numpy(index_unsort).to(device)
        sequences_output = sequences_output.index_select(
            0, index_unsort.clone().detach()
        )

        return sequences_output, self.hidden

    def init_hidden(
        self, batch_size: int
    ) -> tuple[torch.Tensor, torch.Tensor]:
        h_0 = torch.zeros(
            [2, batch_size, self.hidden_size // 2], requires_grad=True
        ).to(device)
        c_0 = torch.zeros(
            [2, batch_size, self.hidden_size // 2], requires_grad=True
        ).to(device)

        return (h_0, c_0)


class Attn(nn.Module):  # type: ignore[misc]
    method: str
    hidden_size: int
    attn: nn.Linear
    other: nn.Parameter

    def __init__(self, method: str, hidden_size: int) -> None:
        super().__init__()

        self.method: str = method
        self.hidden_size: int = hidden_size

        if self.method == "general":
            self.attn: nn.Linear = nn.Linear(self.hidden_size, hidden_size)

        elif self.method == "concat":
            self.attn = nn.Linear(self.hidden_size * 2, hidden_size)
            self.other: nn.Parameter = nn.Parameter(
                torch.FloatTensor(1, hidden_size)
            )

    def forward(
        self,
        hidden: torch.Tensor,
        encoder_outputs: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        # Calculate energies for each encoder output
        if self.method == "dot":
            attn_energies = torch.bmm(
                encoder_outputs, hidden.transpose(1, 2)
            ).squeeze(2)
        elif self.method == "general":
            attn_energies = self.attn(
                encoder_outputs.view(-1, encoder_outputs.size(-1))
            )  # (batch_size * sequence_len, hidden_size)
            attn_energies = torch.bmm(
                attn_energies.view(*encoder_outputs.size()),
                hidden.transpose(1, 2),
            ).squeeze(2)  # (batch_size, sequence_len)
        elif self.method == "concat":
            attn_energies = self.attn(
                torch.cat(
                    (hidden.expand(*encoder_outputs.size()), encoder_outputs),
                    2,
                )
            )  # (batch_size, sequence_len, hidden_size)
            attn_energies = torch.bmm(
                attn_energies,
                self.other.unsqueeze(0).expand(*hidden.size()).transpose(1, 2),
            ).squeeze(2)
        else:
            raise ValueError(
                f"Unsupported attention method: {self.method!r}"
            )

        attn_energies = attn_energies.masked_fill(mask == 0, -1e10)

        # Normalize energies to weights in range 0 to 1
        return F.softmax(attn_energies, 1)


class AttentionDecoder(nn.Module):  # type: ignore[misc]
    vocabulary_size: int
    hidden_size: int
    character_embedding: nn.Embedding
    rnn: nn.LSTM
    attn: Attn
    linear: nn.Linear
    dropout: nn.Dropout

    def __init__(
        self,
        vocabulary_size: int,
        embedding_size: int,
        hidden_size: int,
        dropout: float = 0.5,
    ) -> None:
        """Constructor"""
        super().__init__()
        self.vocabulary_size: int = vocabulary_size
        self.hidden_size: int = hidden_size
        self.character_embedding: nn.Embedding = nn.Embedding(
            vocabulary_size, embedding_size
        )
        self.rnn: nn.LSTM = nn.LSTM(
            input_size=embedding_size + self.hidden_size,
            hidden_size=hidden_size,
            bidirectional=False,
            batch_first=True,
        )

        self.attn: Attn = Attn(method="general", hidden_size=self.hidden_size)
        self.linear: nn.Linear = nn.Linear(hidden_size, vocabulary_size)

        self.dropout: nn.Dropout = nn.Dropout(dropout)

    def forward(
        self,
        input_character: torch.Tensor,
        last_hidden: torch.Tensor,
        encoder_outputs: torch.Tensor,
        mask: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
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


class Seq2Seq(nn.Module):  # type: ignore[misc]
    encoder: Encoder
    decoder: AttentionDecoder
    pad_idx: int
    target_start_token: int
    target_end_token: int
    max_length: int

    def __init__(
        self,
        encoder: Encoder,
        decoder: AttentionDecoder,
        target_start_token: int,
        target_end_token: int,
        max_length: int,
    ) -> None:
        super().__init__()

        self.encoder: Encoder = encoder
        self.decoder: AttentionDecoder = decoder
        self.pad_idx: int = 0
        self.target_start_token: int = target_start_token
        self.target_end_token: int = target_end_token
        self.max_length: int = max_length

        if encoder.hidden_size != decoder.hidden_size:
            raise ValueError(
                f"Encoder and decoder hidden sizes must match. "
                f"Got encoder={encoder.hidden_size}, decoder={decoder.hidden_size}"
            )

    def create_mask(self, source_seq: torch.Tensor) -> torch.Tensor:
        mask = source_seq != self.pad_idx
        return mask

    def forward(
        self,
        source_seq: torch.Tensor,
        source_seq_len: Union[NDArray[Any], list[int]],
        target_seq: Optional[torch.Tensor],
        teacher_forcing_ratio: float = 0.5,
    ) -> torch.Tensor:
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
            if teacher_forcing_ratio != 0:
                raise ValueError(
                    "teacher_forcing_ratio must be zero during inference"
                )
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

            # Non-cryptographic use, pseudo-random generator is acceptable here
            teacher_force = random.random() < teacher_forcing_ratio  # noqa: S311

            decoder_input = (
                target_seq[:, di].reshape(batch_size, 1)
                if teacher_force and target_seq is not None
                else topi.detach()
            )

            if inference and decoder_input == end_token:
                return outputs[:di]

        return outputs


_THAI_G2P: ThaiG2P = ThaiG2P()


def transliterate(text: str) -> str:
    return _THAI_G2P.g2p(text)
