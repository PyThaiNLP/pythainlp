.. currentmodule:: pythainlp.generate

pythainlp.generate
==================
The :class:`pythainlp.generate` module is a powerful tool for generating Thai text using PyThaiNLP. It includes several classes and functions that enable users to create text based on various language models and n-gram models.

Modules
-------

Unigram
~~~~~~~
.. autoclass:: Unigram
   :members:

The :class:`Unigram` class provides functionality for generating text based on unigram language models. Unigrams are single words or tokens, and this class allows you to create text by selecting words probabilistically based on their frequencies in the training data.

Bigram
~~~~~~
.. autoclass:: Bigram
   :members:

The :class:`Bigram` class is designed for generating text using bigram language models. Bigrams are sequences of two words, and this class enables you to generate text by predicting the next word based on the previous word's probability.

Trigram
~~~~~~~
.. autoclass:: Trigram
   :members:

The :class:`Trigram` class extends text generation to trigram language models. Trigrams consist of three consecutive words, and this class facilitates the creation of text by predicting the next word based on the two preceding words' probabilities.

pythainlp.generate.thai2fit.gen_sentence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.generate.thai2fit.gen_sentence
   :noindex:

The function :func:`pythainlp.generate.thai2fit.gen_sentence` offers a convenient way to generate sentences using the Thai2Vec language model. It takes a seed text as input and generates a coherent sentence based on the provided context.

pythainlp.generate.wangchanglm.WangChanGLM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pythainlp.generate.wangchanglm.WangChanGLM
   :members:

The :class:`WangChanGLM` class is a part of the `pythainlp.generate.wangchanglm` module, offering text generation capabilities. It includes methods for creating text using the WangChanGLM language model.

Usage
~~~~~

To use the text generation capabilities provided by the `pythainlp.generate` module, follow these steps:

1. Select the appropriate class or function based on the type of language model you want to use (Unigram, Bigram, Trigram, Thai2Vec, or WangChanGLM).

2. Initialize the selected class or use the function with the necessary parameters.

3. Call the appropriate methods to generate text based on the chosen model.

4. Utilize the generated text for various applications, such as chatbots, content generation, and more.

Example
~~~~~~~

Here's a simple example of how to generate text using the `Unigram` class:

```python
from pythainlp.generate import Unigram

# Initialize the Unigram model
unigram = Unigram()

# Generate a sentence
sentence = unigram.gen_sentence(seed="สวัสดีครับ")

print(sentence)
