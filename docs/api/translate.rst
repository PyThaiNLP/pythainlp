.. currentmodule:: pythainlp.translate

pythainlp.translate
===================
The :mod:`pythainlp.translate` module is dedicated to machine translation capabilities for the PyThaiNLP library. It provides tools for translating text between different languages, making it a valuable resource for natural language processing tasks.

Modules
-------

.. autoclass:: Translate
   :members:
   
   The `Translate` class is the central component of the module, offering a unified interface for various translation tasks. It acts as a coordinator, directing translation requests to specific language pairs and models.

.. autofunction::  pythainlp.translate.en_th.download_model_all
    :noindex:
    
    This function facilitates the download of all available English to Thai translation models. It ensures that the required models are accessible for translation tasks, enhancing the usability of the module.

.. autoclass::  pythainlp.translate.en_th.EnThTranslator
    :members:
    
    The `EnThTranslator` class specializes in translating text from English to Thai. It offers a range of methods for translating sentences and text, enabling accurate and meaningful translations between these languages.

.. autoclass::  pythainlp.translate.en_th.ThEnTranslator
    :members:
    
    Conversely, the `ThEnTranslator` class focuses on translating text from Thai to English. It provides functionality for translating Thai text into English, contributing to effective language understanding and communication.

.. autoclass::  pythainlp.translate.zh_th.ThZhTranslator
    :members:
    
    The `ThZhTranslator` class specializes in translating text from Thai to Chinese (Simplified). This class is valuable for bridging language gaps between these two languages, promoting cross-cultural communication.

.. autoclass::  pythainlp.translate.zh_th.ZhThTranslator
    :members:
    
    The `ZhThTranslator` class is designed for translating text from Chinese (Simplified) to Thai. It assists in making content accessible to Thai-speaking audiences by converting Chinese text into Thai.

.. autoclass::  pythainlp.translate.th_fr.ThFrTranslator
    :members:
    
    Lastly, the `ThFrTranslator` class specializes in translating text from Thai to French. It serves as a tool for expanding language accessibility and promoting content sharing in French-speaking communities.

.. The `pythainlp.translate` module extends the language processing capabilities of PyThaiNLP, offering machine translation functionality for various language pairs. Whether you need to translate text between English and Thai, Thai and Chinese, or Thai and French, this module provides the necessary tools and classes to facilitate seamless language conversion. The `Translate` class acts as the central coordinator, while language-specific classes ensure accurate and meaningful translations for diverse linguistic scenarios.
