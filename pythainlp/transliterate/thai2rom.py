# -*- coding: utf-8 -*-
"""
Romanization of Thai words based on machine-learnt engine ("thai2rom")
"""
import numpy as np
from keras.layers import Input
from keras.models import Model, load_model
from pythainlp.corpus import download, get_corpus_path


class ThaiTransliterator:
    def __init__(self):
        """
        Transliteration of Thai words
        Now supports Thai to Latin (romanization)
        """
        self.__batch_size = 64
        self.__epochs = 100
        self.__latent_dim = 256
        self.__num_samples = 648241
        self.__data_path = get_corpus_path("thai2rom-dataset")
        if not self.__data_path:
            download("thai2rom-dataset")
            self.__data_path = get_corpus_path("thai2rom-dataset")

        self.__input_texts = []
        self.__target_texts = []
        self.__input_characters = set()
        self.__target_characters = set()

        with open(self.__data_path, "r", encoding="utf-8-sig") as self.__fh:
            self.__lines = self.__fh.read().split("\n")

        for line in self.__lines[: min(self.__num_samples, len(self.__lines) - 1)]:
            input_text, target_text = line.split("\t")
            if len(input_text) < 30 and len(target_text) < 90:
                target_text = "\t" + target_text + "\n"
                self.__input_texts.append(input_text)
                self.__target_texts.append(target_text)
                for char in input_text:
                    if char not in self.__input_characters:
                        self.__input_characters.add(char)
                for char in target_text:
                    if char not in self.__target_characters:
                        self.__target_characters.add(char)

        self.__input_characters = sorted(list(self.__input_characters))
        self.__target_characters = sorted(list(self.__target_characters))
        self.__num_encoder_tokens = len(self.__input_characters)
        self.__num_decoder_tokens = len(self.__target_characters)
        self.__max_encoder_seq_length = max([len(text) for text in self.__input_texts])
        self.__max_decoder_seq_length = max([len(text) for text in self.__target_texts])
        """print('Number of samples:', len(self.input_texts))
        print('Number of unique input tokens:', self.num_encoder_tokens)
        print('Number of unique output tokens:', self.num_decoder_tokens)
        print('Max sequence length for inputs:', self.max_encoder_seq_length)
        print('Max sequence length for outputs:', self.max_decoder_seq_length)"""
        self.__input_token_index = dict(
            [(char, i) for i, char in enumerate(self.__input_characters)]
        )
        self.__target_token_index = dict(
            [(char, i) for i, char in enumerate(self.__target_characters)]
        )
        self.__encoder_input_data = np.zeros(
            (
                len(self.__input_texts),
                self.__max_encoder_seq_length,
                self.__num_encoder_tokens,
            ),
            dtype="float32",
        )
        for i, input_text in enumerate(self.__input_texts):
            for t, char in enumerate(input_text):
                self.__encoder_input_data[i, t, self.__input_token_index[char]] = 1.

        # Restore the model and construct the encoder and decoder.
        self.__filemodel = get_corpus_path("thai2rom")
        if not self.__filemodel:
            download("thai2rom")
            self.__filemodel = get_corpus_path("thai2rom")
        self.__model = load_model(self.__filemodel)
        self.__encoder_inputs = self.__model.input[0]  # input_1
        self.__encoder_outputs, self.__state_h_enc, self.__state_c_enc = self.__model.layers[
            2
        ].output  # lstm_1
        self.__encoder_states = [self.__state_h_enc, self.__state_c_enc]
        self.__encoder_model = Model(self.__encoder_inputs, self.__encoder_states)
        self.__decoder_inputs = self.__model.input[1]  # input_2
        self.__decoder_state_input_h = Input(shape=(self.__latent_dim,), name="input_3")
        self.__decoder_state_input_c = Input(shape=(self.__latent_dim,), name="input_4")
        self.__decoder_states_inputs = [
            self.__decoder_state_input_h,
            self.__decoder_state_input_c,
        ]
        self.__decoder_lstm = self.__model.layers[3]
        self.__decoder_outputs, self.__state_h_dec, self.__state_c_dec = self.__decoder_lstm(
            self.__decoder_inputs, initial_state=self.__decoder_states_inputs
        )
        self.__decoder_states = [self.__state_h_dec, self.__state_c_dec]
        self.__decoder_dense = self.__model.layers[4]
        self.__decoder_outputs = self.__decoder_dense(self.__decoder_outputs)
        self.__decoder_model = Model(
            [self.__decoder_inputs] + self.__decoder_states_inputs,
            [self.__decoder_outputs] + self.__decoder_states,
        )

        self.__reverse_input_char_index = dict(
            (i, char) for char, i in self.__input_token_index.items()
        )
        self.__reverse_target_char_index = dict(
            (i, char) for char, i in self.__target_token_index.items()
        )

    def __decode_sequence(self, input_seq):
        self.__states_value = self.__encoder_model.predict(input_seq)
        self.__target_seq = np.zeros((1, 1, self.__num_decoder_tokens))
        self.__target_seq[0, 0, self.__target_token_index["\t"]] = 1.
        self.__stop_condition = False
        self.__decoded_sentence = ""

        while not self.__stop_condition:
            self.__output_tokens, self.__h, self.__c = self.__decoder_model.predict(
                [self.__target_seq] + self.__states_value
            )
            self.__sampled_token_index = np.argmax(self.__output_tokens[0, -1, :])
            self.__sampled_char = self.__reverse_target_char_index[
                self.__sampled_token_index
            ]
            self.__decoded_sentence += self.__sampled_char
            if (
                self.__sampled_char == "\n"
                or len(self.__decoded_sentence) > self.__max_decoder_seq_length
            ):
                self.__stop_condition = True
            self.__target_seq = np.zeros((1, 1, self.__num_decoder_tokens))
            self.__target_seq[0, 0, self.__sampled_token_index] = 1.
            self.__states_value = [self.__h, self.__c]
        return self.__decoded_sentence

    def __encode_input(self, name):
        self.__test_input = np.zeros(
            (1, self.__max_encoder_seq_length, self.__num_encoder_tokens),
            dtype="float32",
        )
        for t, char in enumerate(name):
            self.__test_input[0, t, self.__input_token_index[char]] = 1.
        return self.__test_input

    def romanize(self, text):
        """
        :param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text should read.
        """
        return self.__decode_sequence(self.__encode_input(text))


_THAI_TO_ROM = ThaiTransliterator()


def romanize(text: str) -> str:
    return _THAI_TO_ROM.romanize(text)
