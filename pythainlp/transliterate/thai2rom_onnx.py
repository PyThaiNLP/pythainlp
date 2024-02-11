# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Romanization of Thai words based on machine-learnt engine in ONNX runtime ("thai2rom")
"""
import json
import numpy as np
from onnxruntime import InferenceSession
from pythainlp.corpus import get_corpus_path


_MODEL_ENCODER_NAME = "thai2rom_encoder_onnx"
_MODEL_DECODER_NAME = "thai2rom_decoder_onnx"
_MODEL_CONFIG_NAME = "thai2rom_config_onnx"


class ThaiTransliterator_ONNX:
    def __init__(self):
        """
        Transliteration of Thai words.

        Now supports Thai to Latin (romanization)
        """
        # get the model, download it if it's not available locally
        self.__encoder_filename = get_corpus_path(_MODEL_ENCODER_NAME)
        self.__decoder_filename = get_corpus_path(_MODEL_DECODER_NAME)
        self.__config_filename = get_corpus_path(_MODEL_CONFIG_NAME)

        # loader = torch.load(self.__model_filename, map_location=device)
        with open(str(self.__config_filename)) as f:
            loader = json.load(f)

        OUTPUT_DIM = loader["output_dim"]

        self._maxlength = 100

        self._char_to_ix = loader["char_to_ix"]
        self._ix_to_char = loader["ix_to_char"]
        self._target_char_to_ix = loader["target_char_to_ix"]
        self._ix_to_target_char = loader["ix_to_target_char"]

        # encoder/ decoder
        # Load encoder decoder onnx models.
        self._encoder = InferenceSession(self.__encoder_filename)

        self._decoder = InferenceSession(self.__decoder_filename)

        self._network = Seq2Seq_ONNX(
            self._encoder,
            self._decoder,
            self._target_char_to_ix["<start>"],
            self._target_char_to_ix["<end>"],
            self._maxlength,
            target_vocab_size=OUTPUT_DIM,
        )

    def _prepare_sequence_in(self, text: str):
        """
        Prepare input sequence for ONNX
        """
        idxs = []
        for ch in text:
            if ch in self._char_to_ix:
                idxs.append(self._char_to_ix[ch])
            else:
                idxs.append(self._char_to_ix["<UNK>"])
        idxs.append(self._char_to_ix["<end>"])
        return np.array(idxs)

    def romanize(self, text: str) -> str:
        """
        :param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text
                 should be pronounced.
        """
        input_tensor = self._prepare_sequence_in(text).reshape(1, -1)
        input_length = [len(text) + 1]
        target_tensor_logits = self._network.run(input_tensor, input_length)

        # Seq2seq model returns <END> as the first token,
        # As a result, target_tensor_logits.size() is torch.Size([0])
        if target_tensor_logits.shape[0] == 0:
            target = ["<PAD>"]
        else:
            target_tensor = np.argmax(target_tensor_logits.squeeze(1), 1)
            target = [self._ix_to_target_char[str(t)] for t in target_tensor]

        return "".join(target)


class Seq2Seq_ONNX:
    def __init__(
        self,
        encoder,
        decoder,
        target_start_token,
        target_end_token,
        max_length,
        target_vocab_size,
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

    def run(self, source_seq, source_seq_len):
        # source_seq: (batch_size, MAX_LENGTH)
        # source_seq_len: (batch_size, 1)
        # target_seq: (batch_size, MAX_LENGTH)

        batch_size = source_seq.shape[0]
        start_token = self.target_start_token
        end_token = self.target_end_token
        max_len = self.max_length
        # target_vocab_size = self.decoder.vocabulary_size

        outputs = np.zeros((max_len, batch_size, self.target_vocab_size))

        expected_encoder_outputs = list(
            map(lambda output: output.name, self.encoder.get_outputs())
        )
        encoder_outputs, encoder_hidden, _ = self.encoder.run(
            input_feed={
                "input_tensor": source_seq,
                "input_lengths": source_seq_len,
            },
            output_names=expected_encoder_outputs,
        )

        decoder_input = np.array([[start_token] * batch_size]).reshape(
            batch_size, 1
        )
        encoder_hidden_h_t = np.expand_dims(
            np.concatenate(
                # [encoder_hidden_1, encoder_hidden_2], dim=1
                (encoder_hidden[0], encoder_hidden[1]),
                axis=1,
            ),
            axis=0,
        )
        decoder_hidden = encoder_hidden_h_t

        max_source_len = encoder_outputs.shape[1]
        mask = self.create_mask(source_seq[:, 0:max_source_len])

        for di in range(max_len):
            decoder_output, decoder_hidden = self.decoder.run(
                input_feed={
                    "decoder_input": decoder_input.astype("int32"),
                    "decoder_hidden_1": decoder_hidden,
                    "encoder_outputs": encoder_outputs,
                    "mask": mask.tolist(),
                },
                output_names=[
                    self.decoder.get_outputs()[0].name,
                    self.decoder.get_outputs()[1].name,
                ],
            )

            topi = np.argmax(decoder_output, axis=1)
            outputs[di] = decoder_output

            decoder_input = np.array([topi])

            if decoder_input == end_token:
                return outputs[:di]

        return outputs


_THAI_TO_ROM_ONNX = ThaiTransliterator_ONNX()


def romanize(text: str) -> str:
    return _THAI_TO_ROM_ONNX.romanize(text)
