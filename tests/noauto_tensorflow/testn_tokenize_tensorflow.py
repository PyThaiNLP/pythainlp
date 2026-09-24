# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that require TensorFlow
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (TensorFlow ~1-2 GB)
# - Potential version conflicts with PyTorch
# - Python 3.13+ compatibility issues

# NOTE: deepcut tokenizer was migrated to ONNX and moved to
# tests/noauto_onnx/testn_tokenize_onnx.py
