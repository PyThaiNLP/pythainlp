---
SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# PyThaiNLP Development Notebooks

This directory contains Jupyter notebooks used for **development and testing purposes**. These notebooks are **not** intended for end-users and are primarily used by developers to:

- Test new features and models
- Develop ONNX model conversions
- Experiment with algorithms
- Debug and validate module functionality

## Notebooks Overview

### Testing Notebooks

These notebooks test specific module functionality:

- `test_aksonhan.ipynb` - Testing ancient Thai script conversion
- `test_chat.ipynb` - Testing chatbot functionality with WangChanGLM
- `test_el.ipynb` - Testing entity linking
- `test_gzip_classify.ipynb` - Testing GZIP-based classification
- `test_tcc.ipynb` - Testing Thai Character Cluster tokenization
- `test_wangchanglm.ipynb` - Testing WangChanGLM text generation
- `test_wsd.ipynb` - Testing word sense disambiguation

### Development Tools

These notebooks are used for building and preparing models:

- `convert_thai2rom_to_onnx.ipynb` - Convert Thai romanization models to ONNX format
- `clean_dict.ipynb` - Dictionary cleaning and preprocessing
- `create_words.ipynb` - Word list creation and curation
- `word_detokenize.ipynb` - Testing word detokenization

## For End-Users

If you're looking for examples and tutorials on how to use PyThaiNLP, please visit:

- **Official Tutorials**: <https://pythainlp.org/tutorials>
- **Get Started Guide**: <https://pythainlp.org/tutorials/notebooks/pythainlp_get_started.html>
- **Documentation**: <https://pythainlp.org/docs>
- **Example Scripts**: See the `/examples` directory in the repository root

## Note

These notebooks may:

- Require additional dependencies not installed by default
- Use experimental or development-only features
- Contain incomplete or work-in-progress code
- Not be regularly maintained or updated
