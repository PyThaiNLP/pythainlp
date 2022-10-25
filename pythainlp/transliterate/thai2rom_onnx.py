# -*- coding: utf-8 -*-
"""
Romanization of Thai words based on machine-learnt engine ("thai2rom")
"""

import random

import torch
import torch.nn as nn
import torch.nn.functional as F
from pythainlp.corpus import get_corpus_path

from onnxruntime import InferenceSession

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

_MODEL_NAME = "thai2rom-pytorch-attn"

class ThaiTransliterator_ONNX:
    def __init__(self):
        """
        Transliteration of Thai words.

        Now supports Thai to Latin (romanization)
        """
        # get the model, will download if it's not available locally
        self.__model_filename = get_corpus_path(_MODEL_NAME)

        loader = torch.load(self.__model_filename, map_location=device)

        # INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT = loader["encoder_params"]
        OUTPUT_DIM = loader["decoder_params"][0]

        self._maxlength = 100

        self._char_to_ix = loader["char_to_ix"]
        self._ix_to_char = loader["ix_to_char"]
        self._target_char_to_ix = loader["target_char_to_ix"]
        self._ix_to_target_char = loader["ix_to_target_char"]

        # encoder/ decoder
        # Restore the model and construct the encoder and decoder.
        # self._encoder = Encoder(INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT)
        self._encoder = InferenceSession('./thai2rom_encoder.onnx')

        self._decoder = InferenceSession('./thai2rom_decoder.onnx')

        self._network = Seq2Seq_ONNX(
            self._encoder,
            self._decoder,
            self._target_char_to_ix["<start>"],
            self._target_char_to_ix["<end>"],
            self._maxlength,
            target_vocab_size=OUTPUT_DIM
        )
    
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
        target_tensor_logits = self._network.run(
            input_tensor, input_length
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


class Seq2Seq_ONNX:
    def __init__(
        self,
        encoder,
        decoder,
        target_start_token,
        target_end_token,
        max_length,
        target_vocab_size
    ):
        super().__init__()

        self.encoder = encoder
        self.decoder = decoder
        self.pad_idx = 0
        self.target_start_token = target_start_token
        self.target_end_token = target_end_token
        self.max_length = max_length

        self.target_vocab_size = target_vocab_size

    def create_mask(self, source_seq):
        mask = source_seq != self.pad_idx
        return mask

    def run(
        self, source_seq, source_seq_len
    ):
        # source_seq: (batch_size, MAX_LENGTH)
        # source_seq_len: (batch_size, 1)
        # target_seq: (batch_size, MAX_LENGTH)

        batch_size = source_seq.size(0)
        start_token = self.target_start_token
        end_token = self.target_end_token
        max_len = self.max_length
        # target_vocab_size = self.decoder.vocabulary_size

        outputs = torch.zeros(max_len, batch_size, self.target_vocab_size).to(
            device
        )
        
        expected_encoder_outputs = list(map(lambda output: output.name, self.encoder.get_outputs()))
        encoder_outputs, encoder_hidden, _ = self.encoder.run(
            input_feed = {
                'input_tensor': source_seq.numpy(),
                'input_lengths': source_seq_len.numpy()
            },
            output_names = expected_encoder_outputs
        )
        #@Todo: Remove torch
        encoder_outputs = torch.Tensor(encoder_outputs)
        encoder_hidden = torch.Tensor(encoder_hidden)

        decoder_input = (
            torch.tensor([[start_token] * batch_size])
            .view(batch_size, 1)
            .to(device)
        )
        encoder_hidden_h_t = torch.cat(
            # [encoder_hidden_1, encoder_hidden_2], dim=1
            [encoder_hidden[0], encoder_hidden[1]], dim=1
        ).unsqueeze(dim=0)
        decoder_hidden = encoder_hidden_h_t

        max_source_len = encoder_outputs.size(1)
        mask = self.create_mask(source_seq[:, 0:max_source_len])


        for di in range(max_len):
            decoder_output, decoder_hidden = self.decoder.run(
                input_feed={
                    'decoder_input': decoder_input.numpy().astype('int32'),
                    'decoder_hidden_1': decoder_hidden.numpy(),
                    'encoder_outputs': encoder_outputs.numpy(),
                    'mask': mask.numpy().tolist()
                },
                output_names= [self.decoder.get_outputs()[0].name, self.decoder.get_outputs()[1].name]
            )
            decoder_output = torch.Tensor(decoder_output)
            decoder_hidden = torch.Tensor(decoder_hidden)

            topv, topi = decoder_output.topk(1)
            outputs[di] = decoder_output.to(device)

            decoder_input = (topi.detach())

            if decoder_input == end_token:
                return outputs[:di]

        return outputs

_THAI_TO_ROM_ONNX = ThaiTransliterator_ONNX()

def romanize(text: str) -> str:
    return _THAI_TO_ROM_ONNX.romanize(text)
