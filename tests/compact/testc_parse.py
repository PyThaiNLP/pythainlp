# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
import warnings
from unittest import mock

from pythainlp.chunk import CRFChunkParser, chunk_parse
from pythainlp.tag import pos_tag


class ChunkParseTestCaseC(unittest.TestCase):
    def test_chunk_parse(self):
        tokens = ["ผม", "รัก", "คุณ"]

        w_p = pos_tag(tokens, engine="perceptron", corpus="orchid")
        self.assertIsNotNone(chunk_parse(w_p))

    def test_crf_chunk_parser(self):
        tokens = ["ผม", "รัก", "คุณ"]
        w_p = pos_tag(tokens, engine="perceptron", corpus="orchid")
        with CRFChunkParser() as parser:
            result = parser.parse(w_p)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), len(tokens))

    def test_deprecated_tag_chunk_parse(self):
        """pythainlp.tag.chunk_parse still works but emits DeprecationWarning."""
        from pythainlp.tag import chunk_parse as old_chunk_parse

        tokens = ["ผม", "รัก", "คุณ"]
        w_p = pos_tag(tokens, engine="perceptron", corpus="orchid")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_chunk_parse(w_p)
        self.assertIsNotNone(result)
        self.assertTrue(
            any(
                issubclass(warning.category, DeprecationWarning)
                for warning in w
            )
        )

    def test_deprecated_crfchunk(self):
        """pythainlp.tag.crfchunk.CRFchunk still works but emits DeprecationWarning."""
        from pythainlp.tag.crfchunk import CRFchunk

        tokens = ["ผม", "รัก", "คุณ"]
        w_p = pos_tag(tokens, engine="perceptron", corpus="orchid")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            chunker = CRFchunk()
        self.assertTrue(
            any(
                issubclass(warning.category, DeprecationWarning)
                for warning in w
            )
        )
        result = chunker.parse(w_p)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), len(tokens))

    def test_crf_chunk_parser_exit_ignores_cleanup_error(self):
        parser = CRFChunkParser()
        real_ctx = parser._model_file_ctx
        failing_ctx = mock.MagicMock()
        failing_ctx.__exit__.side_effect = OSError("cleanup failed")
        parser._model_file_ctx = failing_ctx
        try:
            parser.__exit__(None, None, None)  # must not raise
            failing_ctx.__exit__.assert_called_once()
            # The context is kept, so a later exit can retry.
            self.assertIs(parser._model_file_ctx, failing_ctx)
        finally:
            parser._model_file_ctx = real_ctx
            parser.__exit__(None, None, None)
        self.assertIsNone(parser._model_file_ctx)
