# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import numpy as np
    import keras
except ImportError:
    from pythainlp.tools import install_package
    install_package('keras')
    install_package('numpy')

from pythainlp.corpus import get_file,download

from keras.models import Model, load_model
from keras.layers import Input
import numpy as np
class thai2rom:
    def __init__(self):
        '''
        Thai2Rom
        '''
        self.batch_size = 64
        self.epochs = 100
        self.latent_dim = 256
        self.num_samples = 648241
        self.data_path = get_file('thai2rom-dataset')
        if self.data_path==None:
            download('thai2rom-dataset')
            self.data_path = get_file('thai2rom-dataset')
        self.input_texts = []
        self.target_texts = []
        self.input_characters = set()
        self.target_characters = set()
        with open(self.data_path, 'r', encoding='utf-8-sig') as self.f:
            self.lines = self.f.read().split('\n')
        for self.line in self.lines[: min(self.num_samples, len(self.lines) - 1)]:
            self.input_text, self.target_text = self.line.split('\t')
            if len(self.input_text)<30 and len(self.target_text)<90:
                self.target_text = '\t' + self.target_text + '\n'
                self.input_texts.append(self.input_text)
                self.target_texts.append(self.target_text)
                for self.char in self.input_text:
                    if self.char not in self.input_characters:
                        self.input_characters.add(self.char)
                for self.char in self.target_text:
                    if self.char not in self.target_characters:
                        self.target_characters.add(self.char)
        self.input_characters = sorted(list(self.input_characters))
        self.target_characters = sorted(list(self.target_characters))
        self.num_encoder_tokens = len(self.input_characters)
        self.num_decoder_tokens = len(self.target_characters)
        self.max_encoder_seq_length = max([len(self.txt) for self.txt in self.input_texts])
        self.max_decoder_seq_length = max([len(self.txt) for self.txt in self.target_texts])
        '''print('Number of samples:', len(self.input_texts))
        print('Number of unique input tokens:', self.num_encoder_tokens)
        print('Number of unique output tokens:', self.num_decoder_tokens)
        print('Max sequence length for inputs:', self.max_encoder_seq_length)
        print('Max sequence length for outputs:', self.max_decoder_seq_length)'''
        self.input_token_index = dict([(char, i) for i, char in enumerate(self.input_characters)])
        self.target_token_index = dict([(char, i) for i, char in enumerate(self.target_characters)])
        self.encoder_input_data = np.zeros((len(self.input_texts), self.max_encoder_seq_length, self.num_encoder_tokens),dtype='float32')
        for i, input_text in enumerate(self.input_texts):
            for t, char in enumerate(self.input_text):
                self.encoder_input_data[i, t, self.input_token_index[char]] = 1.
        # Restore the model and construct the encoder and decoder.
        self.filemodel=get_file('thai2rom')
        if self.filemodel==None:
            download('thai2rom')
            self.filemodel=get_file('thai2rom')
        self.model = load_model(self.filemodel)
        self.encoder_inputs = self.model.input[0]   # input_1
        self.encoder_outputs, self.state_h_enc, self.state_c_enc = self.model.layers[2].output   # lstm_1
        self.encoder_states = [self.state_h_enc, self.state_c_enc]
        self.encoder_model = Model(self.encoder_inputs, self.encoder_states)
        self.decoder_inputs = self.model.input[1]   # input_2
        self.decoder_state_input_h = Input(shape=(self.latent_dim,), name='input_3')
        self.decoder_state_input_c = Input(shape=(self.latent_dim,), name='input_4')
        self.decoder_states_inputs = [self.decoder_state_input_h, self.decoder_state_input_c]
        self.decoder_lstm = self.model.layers[3]
        self.decoder_outputs, self.state_h_dec, self.state_c_dec = self.decoder_lstm(self.decoder_inputs, initial_state=self.decoder_states_inputs)
        self.decoder_states = [self.state_h_dec, self.state_c_dec]
        self.decoder_dense = self.model.layers[4]
        self.decoder_outputs = self.decoder_dense(self.decoder_outputs)
        self.decoder_model = Model([self.decoder_inputs] + self.decoder_states_inputs,[self.decoder_outputs] + self.decoder_states)

        self.reverse_input_char_index = dict((i, char) for char, i in self.input_token_index.items())
        self.reverse_target_char_index = dict((i, char) for char, i in self.target_token_index.items())
    def decode_sequence(self,input_seq):
        self.states_value = self.encoder_model.predict(input_seq)
        self.target_seq = np.zeros((1, 1, self.num_decoder_tokens))
        self.target_seq[0, 0, self.target_token_index['\t']] = 1.
        self.stop_condition = False
        self.decoded_sentence = ''
        while not self.stop_condition:
            self.output_tokens, self.h, self.c = self.decoder_model.predict([self.target_seq] + self.states_value)
            self.sampled_token_index = np.argmax(self.output_tokens[0, -1, :])
            self.sampled_char = self.reverse_target_char_index[self.sampled_token_index]
            self.decoded_sentence += self.sampled_char
            if (self.sampled_char == '\n' or len(self.decoded_sentence) > self.max_decoder_seq_length):
                self.stop_condition = True
            self.target_seq = np.zeros((1, 1, self.num_decoder_tokens))
            self.target_seq[0, 0, self.sampled_token_index] = 1.
            self.states_value = [self.h, self.c]
        return self.decoded_sentence
    def encode_input(self,name):
        self.test_input = np.zeros((1, self.max_encoder_seq_length, self.num_encoder_tokens),dtype='float32')
        for t, char in enumerate(name):
            self.test_input[0, t, self.input_token_index[char]] = 1.
        return self.test_input
    def romanization(self,text):
        '''
        :param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text should read.
        '''
        return self.decode_sequence(self.encode_input(text))
