# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Romanization of Thai words based on machine-learnt engine in ONNX runtime ("thai2rom")"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, cast

from onnxruntime import InferenceSession

from pythainlp.corpus import get_corpus_path

if TYPE_CHECKING:
    from typing import Dict, List

    import numpy as np
    from numpy.typing import NDArray

_MODEL_ENCODER_NAME: str = "thai2rom_encoder_onnx"
_MODEL_DECODER_NAME: str = "thai2rom_decoder_onnx"
_MODEL_CONFIG_NAME: str = "thai2rom_config_onnx"


class ThaiTransliterator_ONNX:
    def __init__(self) -> None:
        """Transliteration of Thai words.

        Now supports Thai to Latin (romanization)
        """
        # get the model, download it if it's not available locally
        self.__encoder_filename: str = get_corpus_path(_MODEL_ENCODER_NAME)  # type: ignore[assignment]
        self.__decoder_filename: str = get_corpus_path(_MODEL_DECODER_NAME)  # type: ignore[assignment]
        self.__config_filename: str = get_corpus_path(_MODEL_CONFIG_NAME)  # type: ignore[assignment]
        if (
            not self.__encoder_filename
            or not self.__decoder_filename
            or not self.__config_filename
        ):
            missing = [
                n
                for n, v in (
                    (_MODEL_ENCODER_NAME, self.__encoder_filename),
                    (_MODEL_DECODER_NAME, self.__decoder_filename),
                    (_MODEL_CONFIG_NAME, self.__config_filename),
                )
                if not v
            ]
            raise FileNotFoundError(
                f"corpus-not-found names={missing!r}\n"
                f"  Corpus file(s) not found: {', '.join(missing)}.\n"
                f"  Download each missing corpus:\n"
                + "\n".join(
                    f"    Python: pythainlp.corpus.download('{n}')\n"
                    f"    CLI:    thainlp data get {n}"
                    for n in missing
                )
            )

        # loader = torch.load(self.__model_filename, map_location=device)
        with open(str(self.__config_filename), encoding="utf-8") as f:
            loader = json.load(f)

        OUTPUT_DIM = loader["output_dim"]

        self._maxlength: int = 100

        self._char_to_ix: Dict[str, int] = loader["char_to_ix"]
        self._target_char_to_ix: Dict[str, int] = loader["target_char_to_ix"]
        # JSON keys are always strings; convert to int for index-based lookup.
        self._ix_to_char: Dict[int, str] = {
            int(k): v for k, v in loader["ix_to_char"].items()
        }
        self._ix_to_target_char: Dict[int, str] = {
            int(k): v for k, v in loader["ix_to_target_char"].items()
        }

        # encoder/ decoder
        # Load encoder decoder onnx models.
        self._encoder: InferenceSession = InferenceSession(
            self.__encoder_filename
        )

        self._decoder: InferenceSession = InferenceSession(
            self.__decoder_filename
        )

        self._network: Seq2Seq_ONNX = Seq2Seq_ONNX(
            self._encoder,
            self._decoder,
            self._target_char_to_ix["<start>"],
            self._target_char_to_ix["<end>"],
            self._maxlength,
            target_vocab_size=OUTPUT_DIM,
        )

    def _prepare_sequence_in(self, text: str) -> "NDArray[np.int64]":
        """Prepare an int64 input sequence for the ONNX encoder.

        :param str text: Thai text to encode
        :return: encoded character ids ending with the ``<end>`` token
        :rtype: numpy.typing.NDArray[numpy.int64]
        """
        import numpy as np

        idxs = []
        for ch in text:
            if ch in self._char_to_ix:
                idxs.append(self._char_to_ix[ch])
            else:
                idxs.append(self._char_to_ix["<UNK>"])
        idxs.append(self._char_to_ix["<end>"])
        return np.array(idxs, dtype=np.int64)

    def romanize(self, text: str) -> str:
        """:param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text
                 should be pronounced.
        """
        import numpy as np

        input_tensor = self._prepare_sequence_in(text).reshape(1, -1)
        input_length = [len(text) + 1]
        target_tensor_logits = self._network.run(input_tensor, input_length)

        # Seq2seq model returns <END> as the first token,
        # As a result, target_tensor_logits.size() is torch.Size([0])
        if target_tensor_logits.shape[0] == 0:
            target = ["<PAD>"]
        else:
            target_tensor = np.argmax(target_tensor_logits.squeeze(1), 1)
            target = [self._ix_to_target_char[int(t)] for t in target_tensor]

        return "".join(target)


class Seq2Seq_ONNX:
    encoder: InferenceSession
    decoder: InferenceSession
    pad_idx: int
    target_start_token: int
    target_end_token: int
    max_length: int
    target_vocab_size: int

    def __init__(
        self,
        encoder: InferenceSession,
        decoder: InferenceSession,
        target_start_token: int,
        target_end_token: int,
        max_length: int,
        target_vocab_size: int,
    ) -> None:
        super().__init__()

        self.encoder: "InferenceSession" = encoder
        self.decoder: "InferenceSession" = decoder
        self.pad_idx: int = 0
        self.target_start_token: int = target_start_token
        self.target_end_token: int = target_end_token
        self.max_length: int = max_length

        self.target_vocab_size: int = target_vocab_size

    def create_mask(
        self, source_seq: "NDArray[np.int64]"
    ) -> "NDArray[np.bool_]":
        """Create a boolean mask for non-padding positions.

        :param numpy.typing.NDArray[numpy.int64] source_seq: encoded source
            sequence
        :return: boolean mask where True marks non-padding positions
        :rtype: numpy.typing.NDArray[numpy.bool_]
        """
        mask = source_seq != self.pad_idx
        return cast("NDArray[np.bool_]", mask)

    def run(
        self, source_seq: "NDArray[np.int64]", source_seq_len: List[int]
    ) -> "NDArray[np.float32]":
        """Run ONNX seq2seq decoding and return logits.

        :param numpy.typing.NDArray[numpy.int64] source_seq: encoded source
            sequence with shape ``(batch_size, sequence_length)``
        :param List[int] source_seq_len: unpadded source lengths
        :return: decoder logits as a float32 array with shape
            ``(decoded_length, batch_size, target_vocab_size)``
        :rtype: numpy.typing.NDArray[numpy.float32]
        """
        # source_seq: (batch_size, MAX_LENGTH)
        # source_seq_len: (batch_size, 1)
        # target_seq: (batch_size, MAX_LENGTH)
        import numpy as np

        batch_size = source_seq.shape[0]
        start_token = self.target_start_token
        end_token = self.target_end_token
        max_len = self.max_length
        # target_vocab_size = self.decoder.vocabulary_size

        outputs: "NDArray[np.float32]" = np.zeros(
            (max_len, batch_size, self.target_vocab_size), dtype=np.float32
        )

        expected_encoder_outputs = [
            output.name for output in self.encoder.get_outputs()
        ]
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
            decoder_output_raw, decoder_hidden = self.decoder.run(
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
            decoder_output = cast("NDArray[np.float32]", decoder_output_raw)

            topi = np.argmax(decoder_output, axis=1)
            outputs[di] = decoder_output

            decoder_input = np.array([topi], dtype=np.int64)

            if decoder_input.item() == end_token:
                return outputs[:di]

        return outputs


_THAI_TO_ROM_ONNX: ThaiTransliterator_ONNX = ThaiTransliterator_ONNX()


def romanize(text: str) -> str:
    return _THAI_TO_ROM_ONNX.romanize(text)
