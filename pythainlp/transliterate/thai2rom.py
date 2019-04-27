# -*- coding: utf-8 -*-
"""
Romanization of Thai words based on machine-learnt engine ("thai2rom")
"""
import numpy as np
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model, load_model
from pythainlp.corpus import download, get_corpus_path
class ThaiTransliterator:
    def __init__(self):
        """
        Transliteration of Thai words
        Now supports Thai to Latin (romanization)
        """
        self.__input_token_index = {
         ' ': 0, '!': 1, '"': 2, '(': 3, ')': 4,
         '-': 5, '.': 6, '0': 7, '1': 8, '2': 9,
         '3': 10, '4': 11, '5': 12, '6': 13, '7': 14,
         '8': 15, '9': 16, '\xa0': 17, 'ก': 18, 'ข': 19,
         'ฃ': 20, 'ค': 21, 'ฅ': 22, 'ฆ': 23, 'ง': 24,
         'จ': 25, 'ฉ': 26, 'ช': 27, 'ซ': 28, 'ฌ': 29,
         'ญ': 30, 'ฎ': 31, 'ฏ': 32, 'ฐ': 33, 'ฑ': 34,
         'ฒ': 35, 'ณ': 36, 'ด': 37, 'ต': 38, 'ถ': 39,
         'ท': 40, 'ธ': 41, 'น': 42, 'บ': 43, 'ป': 44,
         'ผ': 45, 'ฝ': 46, 'พ': 47, 'ฟ': 48, 'ภ': 49,
         'ม': 50, 'ย': 51, 'ร': 52, 'ฤ': 53, 'ล': 54,
         'ฦ': 55, 'ว': 56, 'ศ': 57, 'ษ': 58, 'ส': 59,
         'ห': 60, 'ฬ': 61, 'อ': 62, 'ฮ': 63, 'ฯ': 64,
         'ะ': 65, 'ั': 66, 'า': 67, 'ำ': 68, 'ิ': 69,
         'ี': 70, 'ึ': 71, 'ื': 72, 'ุ': 73, 'ู': 74,
         'ฺ': 75, 'เ': 76, 'แ': 77, 'โ': 78, 'ใ': 79,
         'ไ': 80, 'ๅ': 81, 'ๆ': 82, '็': 83, '่': 84,
         '้': 85, '๊': 86, '๋': 87, '์': 88, 'ํ': 89, '๙': 90
        }
        self.__target_token_index = {
         '\t': 0, '\n': 1, ' ': 2, '!': 3, '"': 4,
         '(': 5, ')': 6, '-': 7, '0': 8, '1': 9,
         '2': 10, '3': 11, '4': 12, '5': 13,
         '6': 14, '7': 15, '8': 16, '9': 17, 'a': 18,
         'b': 19, 'c': 20, 'd': 21, 'e': 22, 'f': 23,
         'g': 24, 'h': 25, 'i': 26, 'k': 27, 'l': 28,
         'm': 29, 'n': 30, 'o': 31, 'p': 32, 'r': 33,
         's': 34, 't': 35, 'u': 36, 'w': 37, 'y': 38
        }
        self.__reverse_input_char_index = dict(
         (i, char) for char, i in self.__input_token_index.items()
        )
        self.__reverse_target_char_index = dict(
         (i, char) for char, i in self.__target_token_index.items()
        )
        self.__batch_size = 64
        self.__epochs = 100
        self.__latent_dim = 256
        self.__num_encoder_tokens = 91
        self.__num_decoder_tokens = 39
        self.__max_encoder_seq_length = 20
        self.__max_decoder_seq_length = 22

        # Restore the model and construct the encoder and decoder.
        self.__filemodel = get_corpus_path("thai2rom-v2")
        if not self.__filemodel:
            download("thai2rom-v2")
            self.__filemodel = get_corpus_path("thai2rom-v2")
        self.__model = load_model(self.__filemodel)
        self.__encoder_inputs = self.__model.input[0]  # input_1
        self.__encoder_outputs, self.__state_h_enc, self.__state_c_enc = self.__model.layers[
            2
        ].output  # lstm_1
        self.__encoder_states = [self.__state_h_enc, self.__state_c_enc]
        self.__encoder_model = Model(
            self.__encoder_inputs, self.__encoder_states
        )
        self.__decoder_inputs = self.__model.input[1]  # input_2
        self.__decoder_state_input_h = Input(
            shape=(self.__latent_dim,), name="input_3"
        )
        self.__decoder_state_input_c = Input(
            shape=(self.__latent_dim,), name="input_4"
        )
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
            self.__sampled_token_index = np.argmax(
                self.__output_tokens[0, -1, :]
            )
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
        :return: English (more or less) text that spells out how the Thai text should be pronounced.
        """
        return self.__decode_sequence(self.__encode_input(text)).strip()

_THAI_TO_ROM = ThaiTransliterator()


def romanize(text: str) -> str:
    return _THAI_TO_ROM.romanize(text)
