# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Test CRFsuite dump conversion helpers."""

import tempfile
import unittest
from pathlib import Path

from build_tools.convert_crf_to_weights import parse_dump_file


class ConvertCrfToWeightsTestCase(unittest.TestCase):
    def _parse_dump(
        self, content: str
    ) -> tuple[list[str], dict[str, float], dict[str, dict[str, float]]]:
        with tempfile.TemporaryDirectory() as temp_dir:
            dump_path = Path(temp_dir) / "model.dump"
            dump_path.write_text(content, encoding="utf-8")
            return parse_dump_file(str(dump_path))

    def test_parses_labels_transitions_and_state_features(self) -> None:
        labels, transitions, state_features = self._parse_dump(
            """LABELS = {
0: O
1: B-X
label continuation
2:B-Y
}
TRANSITIONS = {
(0) O --> B-X: -1.25e+2
(1) A --> B --> C: +0.5
}
STATE_FEATURES = {
(0) word:สวัสดี --> B-X: 2.0
(1) attr --> x --> y: 1e-2
}
"""
        )

        self.assertEqual(labels, ["O", "B-X\nlabel continuation", "B-Y"])
        self.assertEqual(transitions, {"O->B-X": -125.0, "A --> B->C": 0.5})
        self.assertEqual(
            state_features,
            {"word:สวัสดี": {"B-X": 2.0}, "attr": {"x --> y": 0.01}},
        )

    def test_ignores_malformed_weighted_rows(self) -> None:
        content = """UNKNOWN = {
ignored
}
LABELS = {
0: O
invalid label line
}
TRANSITIONS = {
(0) O --> B-X: 1.
(x) O --> B-X: 1
(1) O-->B-X: 1
(2) O --> B-X: 1
}
STATE_FEATURES = {
(0) missing arrow: 1
(1) attr --> label:1
(2) attr -->label: 1
(3) attr --> label: nope
}
"""
        content = content.replace(
            "(2) O --> B-X: 1\n}", "(2) O --> B-X: 1 \n}"
        )
        labels, transitions, state_features = self._parse_dump(content)

        self.assertEqual(labels, ["O\ninvalid label line"])
        self.assertEqual(transitions, {})
        self.assertEqual(state_features, {})

    def test_accepts_empty_labels_section(self) -> None:
        self.assertEqual(
            self._parse_dump("LABELS = {\n}\n"),
            ([], {}, {}),
        )


if __name__ == "__main__":
    unittest.main()
