# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Offline tests for pythainlp.parse."""

import sys
import types
import unittest
from contextlib import ExitStack
from unittest import mock

from pythainlp.parse import core, dependency_parsing


class ParseTestCase(unittest.TestCase):
    def test_unsupported_engine(self) -> None:
        for engine in ("", "unknown", "ESUPAR"):
            with self.subTest(engine=engine):
                with self.assertRaises(NotImplementedError):
                    dependency_parsing("ผมเป็นคนดี", engine=engine)

    def test_engine_is_loaded_once(self) -> None:
        created: list[str] = []

        class FakeParse:
            def __init__(self, model: str = "") -> None:
                created.append(model)

            def __call__(self, text: str, tag: str = "str") -> str:
                return f"{tag}:{text}"

        fake = types.ModuleType("pythainlp.parse.esupar_engine")
        setattr(fake, "Parse", FakeParse)
        with ExitStack() as stack:
            stack.enter_context(
                mock.patch.dict(sys.modules, {fake.__name__: fake})
            )
            stack.enter_context(mock.patch.object(core, "_tagger", None))
            stack.enter_context(mock.patch.object(core, "_tagger_name", ""))
            self.assertEqual(
                dependency_parsing("ผม", model="m", tag="list"), "list:ผม"
            )
            self.assertEqual(dependency_parsing("คุณ"), "str:คุณ")
        self.assertEqual(created, ["m"])  # the second call reuses the engine
