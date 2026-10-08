# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tests for build_tools/onnx_metadata.py.

The version and property helpers run in the core tier. The tests that read
and write ONNX files need the ``onnx`` package and are skipped without it.
"""

import contextlib
import importlib.util
import io
import json
import os
import stat
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import mock

import pythainlp

SCRIPT_PATH = (
    Path(pythainlp.__file__).resolve().parent.parent
    / "build_tools"
    / "onnx_metadata.py"
)
HAS_ONNX = importlib.util.find_spec("onnx") is not None
# The sdist ships tests/ but not build_tools/.
HAS_SCRIPT = SCRIPT_PATH.is_file()
skip_without_script = unittest.skipUnless(
    HAS_SCRIPT, "build_tools is not part of this distribution"
)


def load_script() -> ModuleType:
    """Load the script as a module."""
    spec = importlib.util.spec_from_file_location(
        "onnx_metadata_under_test", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool: Any = load_script() if HAS_SCRIPT else None

# (version, packed integer)
VERSIONS = (
    ("0.0.0", 0),
    ("0.0.1", 1),
    ("1.0.0", 281474976710656),
    ("1.0.1", 281474976710657),
    ("1.2.3", (1 << 48) | (2 << 32) | 3),
    ("32767.65535.4294967295", (1 << 63) - 1),
)

BAD_VERSIONS = (
    "",
    "1",
    "1.0",
    "1.0.0.0",
    "1.0.0-dev",
    "01.0.0",  # leading zeros would not read back as given
    "1.00.0",
    "1.0.00",
    " 1.0.0",
    "1.0.0 ",
    "-1.0.0",
    "a.b.c",
    "１.0.0",  # full-width digit
    "٣.0.0",  # Arabic-Indic digit
    "32768.0.0",
    "0.65536.0",
    "0.0.4294967296",
)


@skip_without_script
class VersionTestCase(unittest.TestCase):
    def test_round_trip(self) -> None:
        for version, packed in VERSIONS:
            with self.subTest(version=version):
                self.assertEqual(tool.semver_to_int(version), packed)
                self.assertEqual(tool.int_to_semver(packed), version)

    def test_bad_versions(self) -> None:
        for version in BAD_VERSIONS:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    tool.semver_to_int(version)

    def test_non_string(self) -> None:
        for value in (None, 1, 1.0):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    tool.semver_to_int(value)


# licenseId -> isDeprecatedLicenseId
LICENSE_IDS = {
    "Apache-2.0": False,
    "BSD-3-Clause": False,
    "CC-BY-4.0": False,
    "GPL-2.0": True,
    "GPL-2.0-only": False,
    "MIT": False,
}

# (given, recorded, warning is expected)
LICENSE_CASES = (
    ("Apache-2.0", "Apache-2.0", False),
    ("GPL-2.0-only", "GPL-2.0-only", False),
    ("apache-2.0", "Apache-2.0", True),
    ("APACHE-2.0", "Apache-2.0", True),
    ("apache 2.0  license ", "Apache-2.0", True),
    ("Apache-2.0 License", "Apache-2.0", True),
    ("BSD 3-Clause Licence", "BSD-3-Clause", True),
    ("  mit", "MIT", True),
    ("MIT\t\n", "MIT", True),
    ("mit LICENSE", "MIT", True),
    ("gpl-2.0-only license", "GPL-2.0-only", True),
    ("GPL-2.0", "GPL-2.0", True),  # deprecated
    ("gpl 2.0 licence", "GPL-2.0", True),  # normalized and deprecated
    ("cc by 4.0", "CC-BY-4.0", True),
    ("CC License ", "CC License", True),
    ("Apache 2", "Apache 2", True),
    ("Apache-2.0 OR MIT", "Apache-2.0 OR MIT", True),
    ("license", "license", True),
    ("-license", "-license", True),
    ("", "", True),
    ("   ", "", True),
    ("ไทย", "ไทย", True),
)


@skip_without_script
class LicenseTestCase(unittest.TestCase):
    def test_normalize(self) -> None:
        cases = (
            ("", ""),
            ("  Apache 2.0  License ", "apache-2.0-license"),
            ("MIT", "mit"),
            ("a\u00a0b\tc\nd", "a-b-c-d"),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(tool.normalize_license(text), expected)

    def test_resolve(self) -> None:
        for given, recorded, warned in LICENSE_CASES:
            with self.subTest(given=given):
                result, warning = tool.resolve_license(given, LICENSE_IDS)
                self.assertEqual(result, recorded)
                self.assertEqual(warning is not None, warned)

    def test_warning_text(self) -> None:
        _, warning = tool.resolve_license("apache 2.0  license ", LICENSE_IDS)
        self.assertIn("'apache 2.0  license '", warning)  # given
        self.assertIn("'Apache-2.0'", warning)  # recorded
        _, warning = tool.resolve_license("CC License ", LICENSE_IDS)
        self.assertIn("'CC License'", warning)
        self.assertIn("not found in the SPDX License List", warning)

    def test_deprecated_id(self) -> None:
        recorded, warning = tool.resolve_license("GPL-2.0", LICENSE_IDS)
        self.assertEqual(recorded, "GPL-2.0")
        self.assertEqual(warning, "'GPL-2.0' is a deprecated SPDX license ID")
        _, warning = tool.resolve_license("gpl 2.0", LICENSE_IDS)
        self.assertIn("was normalized", warning)
        self.assertIn("'GPL-2.0' is a deprecated SPDX license ID", warning)
        for given in ("MIT", "GPL-2.0-only"):
            warning = tool.resolve_license(given, LICENSE_IDS)[1]
            self.assertNotIn("deprecated", warning or "")

    def test_exact_match_wins_over_normalization(self) -> None:
        ids = {"mit": False, "MIT": False}
        self.assertEqual(tool.resolve_license("mit", ids), ("mit", None))
        self.assertEqual(tool.resolve_license("MIT", ids), ("MIT", None))

    def test_first_of_ids_with_the_same_lower_case(self) -> None:
        recorded, _ = tool.resolve_license("Mit", {"MIT": False, "mit": False})
        self.assertEqual(recorded, "MIT")

    def test_empty_list(self) -> None:
        recorded, warning = tool.resolve_license("MIT", {})
        self.assertEqual(recorded, "MIT")
        self.assertIn("not found", warning)

    def test_load_licenses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "licenses.json"
            path.write_text(
                json.dumps(
                    {
                        "licenses": [
                            {"licenseId": "MIT"},
                            {"licenseId": 7},
                            {"name": "no id"},
                            "text",
                            {
                                "licenseId": "GPL-2.0",
                                "isDeprecatedLicenseId": True,
                            },
                            {"licenseId": "A", "isDeprecatedLicenseId": "yes"},
                            {"licenseId": "B", "isDeprecatedLicenseId": False},
                        ]
                    }
                ),
                encoding="utf-8-sig",
            )
            licenses = tool.load_licenses(str(path))
            self.assertEqual(
                licenses,
                {"MIT": False, "GPL-2.0": True, "A": False, "B": False},
            )
            self.assertEqual(list(licenses), ["MIT", "GPL-2.0", "A", "B"])

    def test_load_licenses_errors(self) -> None:
        contents = (
            "not json",
            "[]",
            "{}",
            '{"licenses": "MIT"}',
            '{"licenses": []}',
            '{"licenses": [{"name": "x"}]}',
        )
        with tempfile.TemporaryDirectory() as directory:
            for content in contents:
                with self.subTest(content=content):
                    path = Path(directory) / "licenses.json"
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        tool.load_licenses(str(path))
            with self.assertRaises(OSError):
                tool.load_licenses(str(Path(directory) / "missing.json"))

    def test_only_https_urls(self) -> None:
        for source in ("http://x/y.json", "ftp://x/y.json", "file:///x.json"):
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    tool.load_licenses(source)

    def test_https_download(self) -> None:
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"licenses": [{"licenseId": "MIT"}]}'
        with mock.patch("urllib.request.urlopen", return_value=response) as op:
            ids = tool.load_licenses("https://example.org/licenses.json")
        self.assertEqual(ids, {"MIT": False})
        self.assertEqual(
            op.call_args.args, ("https://example.org/licenses.json",)
        )
        self.assertIn("timeout", op.call_args.kwargs)

    def test_default_list_is_the_spdx_url(self) -> None:
        args = tool.build_parser().parse_args(["set", "m.onnx", "--doc", "x"])
        self.assertEqual(
            args.spdx_list, "https://spdx.org/licenses/licenses.json"
        )


@skip_without_script
class PropTestCase(unittest.TestCase):
    def test_parse_prop(self) -> None:
        cases = (
            ("a=b", ("a", "b")),
            ("a=", ("a", "")),
            ("a=b=c", ("a", "b=c")),
            (
                "source=https://example.org/?q=1",
                ("source", "https://example.org/?q=1"),
            ),
            ("ชื่อ=ไทย", ("ชื่อ", "ไทย")),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(tool.parse_prop(text), expected)

    def test_bad_prop(self) -> None:
        for text in ("", "=", "=v", "novalue"):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    tool.parse_prop(text)


@skip_without_script
@unittest.skipUnless(HAS_ONNX, "the onnx package is not installed")
class FileTestCase(unittest.TestCase):
    def setUp(self) -> None:
        import onnx
        from onnx import TensorProto, helper

        node = helper.make_node("Identity", ["x"], ["y"])
        graph = helper.make_graph(
            [node],
            "tiny",
            [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1])],
            [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1])],
        )
        model = helper.make_model(graph)
        model.model_version = tool.semver_to_int("1.0.0")
        model.domain = "org.example"
        helper.set_model_props(model, {"model_license": "MIT", "keep": "me"})

        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.path = Path(self._dir.name) / "tiny.onnx"
        onnx.save(model, str(self.path))

        # Use a local SPDX License List: the tests must not need a network.
        self._list_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._list_dir.cleanup)
        self.spdx_list = Path(self._list_dir.name) / "licenses.json"
        self.spdx_list.write_text(
            json.dumps(
                {
                    "licenses": [
                        {"licenseId": i, "isDeprecatedLicenseId": d}
                        for i, d in LICENSE_IDS.items()
                    ]
                }
            ),
            encoding="utf-8",
        )
        patcher = mock.patch.object(tool, "SPDX_LIST_URL", str(self.spdx_list))
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_tool(self, *argv: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                status = tool.main(list(argv))
            except SystemExit as exit_:
                status = int(exit_.code or 0)
        return status, out.getvalue(), err.getvalue()

    def show(self) -> dict[str, Any]:
        status, out, _ = self.run_tool("show", "--json", str(self.path))
        self.assertEqual(status, 0)
        info: dict[str, Any] = json.loads(out)[0]
        return info

    def test_show(self) -> None:
        info = self.show()
        self.assertEqual(info["model_version"], "1.0.0")
        self.assertEqual(info["model_version_raw"], 281474976710656)
        self.assertEqual(info["domain"], "org.example")
        self.assertEqual(info["graph_name"], "tiny")
        self.assertEqual(
            info["metadata_props"], {"model_license": "MIT", "keep": "me"}
        )
        status, out, _ = self.run_tool("show", str(self.path))
        self.assertEqual(status, 0)
        self.assertIn("(1.0.0)", out)
        self.assertIn("model_license", out)

    def test_set_keeps_other_metadata(self) -> None:
        status, out, _ = self.run_tool(
            "set",
            str(self.path),
            "--version",
            "1.0.1",
            "--author",
            "นามสมมติ, B",
            "--prop",
            "source=https://example.org",
            "--name",
            "renamed",
            "--doc",
            "A model.",
            "--domain",
            "org.pythainlp",
        )
        self.assertEqual(status, 0)
        self.assertIn("md5", out)
        info = self.show()
        self.assertEqual(info["model_version"], "1.0.1")
        self.assertEqual(info["graph_name"], "renamed")
        self.assertEqual(info["doc_string"], "A model.")
        self.assertEqual(info["domain"], "org.pythainlp")
        self.assertEqual(
            info["metadata_props"],
            {
                "model_license": "MIT",
                "keep": "me",
                "model_author": "นามสมมติ, B",
                "source": "https://example.org",
            },
        )

    def test_license_is_normalized_with_a_warning(self) -> None:
        status, out, err = self.run_tool(
            "set", str(self.path), "--license", "apache 2.0  license "
        )
        self.assertEqual(status, 0)
        self.assertIn("warning: license was normalized", err)
        self.assertIn("'apache 2.0  license '", err)
        self.assertIn("'Apache-2.0'", err)
        self.assertIn("verified", out)
        self.assertEqual(
            self.show()["metadata_props"]["model_license"], "Apache-2.0"
        )

    def test_exact_license_has_no_warning(self) -> None:
        status, _, err = self.run_tool(
            "set", str(self.path), "--license", "Apache-2.0"
        )
        self.assertEqual(status, 0)
        self.assertEqual(err, "")

    def test_deprecated_license_is_recorded_with_a_warning(self) -> None:
        status, _, err = self.run_tool(
            "set", str(self.path), "--license", "GPL-2.0"
        )
        self.assertEqual(status, 0)
        self.assertIn("'GPL-2.0' is a deprecated SPDX license ID", err)
        self.assertEqual(
            self.show()["metadata_props"]["model_license"], "GPL-2.0"
        )

    def test_unknown_license_is_kept_with_a_warning(self) -> None:
        status, _, err = self.run_tool(
            "set", str(self.path), "--license", "CC License "
        )
        self.assertEqual(status, 0)
        self.assertIn("'CC License'", err)
        self.assertIn("not found in the SPDX License List", err)
        self.assertEqual(
            self.show()["metadata_props"]["model_license"], "CC License"
        )

    def test_license_with_a_list_that_cannot_be_read(self) -> None:
        missing = str(self.spdx_list.with_name("missing.json"))
        for source in (missing, "http://example.org/licenses.json"):
            with self.subTest(source=source):
                status, _, err = self.run_tool(
                    "set",
                    str(self.path),
                    "--license",
                    " Apache 2 ",
                    "--spdx-list",
                    source,
                    "--dry-run",
                )
                self.assertEqual(status, 0)
                self.assertIn("SPDX License List is not available", err)
                self.assertIn("'Apache 2'", err)

    def test_license_warning_is_ascii_and_shown_in_a_dry_run(self) -> None:
        before = self.path.read_bytes()
        status, _, err = self.run_tool(
            "set", str(self.path), "--license", "ไทย", "--dry-run"
        )
        self.assertEqual(status, 0)
        self.assertTrue(err.isascii(), err)
        self.assertIn("\\u0e44", err)
        self.assertEqual(self.path.read_bytes(), before)

    def test_set_license_replaces(self) -> None:
        self.run_tool("set", str(self.path), "--license", "Apache-2.0")
        props = self.show()["metadata_props"]
        self.assertEqual(props["model_license"], "Apache-2.0")
        self.assertEqual(props["keep"], "me")

    def test_dry_run_and_no_change_do_not_write(self) -> None:
        before = self.path.read_bytes()
        status, out, _ = self.run_tool(
            "set", str(self.path), "--version", "2.0.0", "--dry-run"
        )
        self.assertEqual(status, 0)
        self.assertIn("dry run", out)
        self.assertEqual(self.path.read_bytes(), before)
        status, out, _ = self.run_tool(
            "set", str(self.path), "--version", "1.0.0", "--license", "MIT"
        )
        self.assertEqual(status, 0)
        self.assertIn("no change", out)
        self.assertEqual(self.path.read_bytes(), before)

    def test_no_temp_file_left(self) -> None:
        self.run_tool("set", str(self.path), "--version", "1.0.1")
        self.assertEqual(
            sorted(p.name for p in self.path.parent.iterdir()), ["tiny.onnx"]
        )

    def test_errors(self) -> None:
        bad = self.path.with_name("bad.onnx")
        bad.write_bytes(b"not an onnx file")
        missing = str(self.path.with_name("missing.onnx"))
        cases = (
            ("show", str(bad)),
            ("show", missing),
            ("set", missing, "--version", "1.0.1"),
            ("set", str(bad), "--version", "1.0.1"),
            ("set", str(self.path), "--version", "1.0"),
            ("set", str(self.path), "--prop", "novalue"),
        )
        for argv in cases:
            with self.subTest(argv=argv):
                status, _, err = self.run_tool(*argv)
                self.assertEqual(status, 1)
                self.assertTrue(err.startswith("Error:"))
        self.assertEqual(self.show()["model_version"], "1.0.0")

    def test_version_that_cannot_be_stored(self) -> None:
        before = self.path.read_bytes()
        for version, hint in (
            ("32768.0.0", "at most 32767"),
            ("0.65536.0", "at most 65535"),
            ("0.0.4294967296", "at most 4294967295"),
            ("1.0.0-dev", "without leading zeros"),
        ):
            with self.subTest(version=version):
                status, _, err = self.run_tool(
                    "set", str(self.path), "--version", version
                )
                self.assertEqual(status, 1)
                self.assertIn("cannot be stored", err)
                self.assertIn(hint, err)
        self.assertEqual(self.path.read_bytes(), before)

    def test_read_back_mismatch_keeps_file(self) -> None:
        from onnx import helper

        real_write = tool._write

        def bump_version(model: Any, path: Path) -> None:
            model.model_version += 1
            real_write(model, path)

        def drop_props(model: Any, path: Path) -> None:
            helper.set_model_props(model, {})
            real_write(model, path)

        def rename_graph(model: Any, path: Path) -> None:
            model.graph.name = "other"
            real_write(model, path)

        before = self.path.read_bytes()
        for writer, key in (
            (bump_version, "model_version"),
            (drop_props, "metadata_props"),
            (rename_graph, "graph_name"),
        ):
            with self.subTest(writer=writer.__name__):
                with mock.patch.object(tool, "_write", writer):
                    status, _, err = self.run_tool(
                        "set", str(self.path), "--version", "1.0.1"
                    )
                self.assertEqual(status, 1)
                self.assertIn("Read-back check failed (file not changed)", err)
                self.assertIn(key, err)
                self.assertEqual(self.path.read_bytes(), before)
                self.assertEqual(
                    [p.name for p in self.path.parent.iterdir()], ["tiny.onnx"]
                )

    def test_read_back_mismatch_after_replace(self) -> None:
        problems = [[], ["domain: given 'a', read back 'b'"]]
        with mock.patch.object(tool, "_mismatches", side_effect=problems):
            status, _, err = self.run_tool(
                "set", str(self.path), "--version", "1.0.1"
            )
        self.assertEqual(status, 1)
        self.assertIn("file was replaced", err)

    def test_verified_message(self) -> None:
        _, out, _ = self.run_tool("set", str(self.path), "--version", "1.0.1")
        self.assertIn("verified", out)

    def test_error_messages_are_ascii(self) -> None:
        missing = str(self.path.with_name("ไทย.onnx"))
        cases = (
            (1, ("set", str(self.path), "--version", "ไทย")),
            (1, ("set", str(self.path), "--prop", "ไทย")),
            (1, ("show", missing)),
            (2, ("ไทย",)),
            (2, ("set", str(self.path), "--ไทย")),
        )
        for expected_status, argv in cases:
            with self.subTest(argv=argv):
                status, _, err = self.run_tool(*argv)
                self.assertEqual(status, expected_status)
                self.assertTrue(err.isascii(), err)
                self.assertIn("\\u0e44", err)

    def test_usage_names_the_onnx_field(self) -> None:
        with mock.patch.dict("os.environ", {"COLUMNS": "200"}):
            status, out, _ = self.run_tool("set", "--help")
        self.assertEqual(status, 0)
        for option, field in (
            ("--author", 'metadata_props["model_author"]'),
            ("--doc", "doc_string"),
            ("--domain", "domain"),
            ("--license", 'metadata_props["model_license"]'),
            ("--name", "graph.name"),
            ("--prop", "metadata_props[KEY]"),
            ("--version", "model_version"),
        ):
            with self.subTest(option=option):
                line = next(
                    (
                        x
                        for x in out.splitlines()
                        if x.strip().startswith(option)
                    ),
                    "",
                )
                self.assertIn("->", line)
                self.assertIn(field, line)

    def test_conflicting_properties(self) -> None:
        before = self.path.read_bytes()
        cases = (
            ("--license", "A", "--prop", "model_license=B"),
            ("--author", "A", "--prop", "model_author=B"),
            ("--prop", "k=1", "--prop", "k=2"),
            ("--prop", "k=1", "--prop", "k=1"),
        )
        for options in cases:
            with self.subTest(options=options):
                status, _, err = self.run_tool("set", str(self.path), *options)
                self.assertEqual(status, 1)
                self.assertIn("more than once", err)
        self.assertEqual(self.path.read_bytes(), before)

    def test_duplicate_property_keys_are_not_rewritten(self) -> None:
        import onnx

        model = onnx.load(str(self.path))
        model.metadata_props.add(key="keep", value="again")
        path = self.path.with_name("duplicate.onnx")
        onnx.save(model, str(path))
        before = path.read_bytes()
        status, _, err = self.run_tool("set", str(path), "--version", "1.0.1")
        self.assertEqual(status, 1)
        self.assertIn("duplicate keys ['keep']", err)
        self.assertEqual(path.read_bytes(), before)

    def test_show_warns_about_duplicate_keys(self) -> None:
        import onnx

        model = onnx.load(str(self.path))
        model.metadata_props.add(key="keep", value="again")
        for value in ("a", "b"):
            model.metadata_props.add(key="ชื่อ", value=value)
        path = self.path.with_name("duplicate.onnx")
        onnx.save(model, str(path))

        status, out, err = self.run_tool("show", "--json", str(path))

        self.assertEqual(status, 0)
        self.assertIn("duplicate metadata_props keys", err)
        self.assertTrue(err.isascii(), err)
        self.assertEqual(
            sorted(json.loads(out)[0]["duplicate_keys"]), ["keep", "ชื่อ"]
        )
        status, out, err = self.run_tool("show", "--json", str(self.path))
        self.assertEqual(err, "")
        self.assertEqual(json.loads(out)[0]["duplicate_keys"], [])

    @unittest.skipIf(
        hasattr(os, "geteuid") and os.geteuid() == 0,
        "root ignores file permissions",
    )
    def test_read_only_file_is_refused(self) -> None:
        before = self.path.read_bytes()
        self.path.chmod(0o444)
        self.addCleanup(self.path.chmod, 0o644)
        for extra in ((), ("--dry-run",)):
            with self.subTest(extra=extra):
                status, _, err = self.run_tool(
                    "set", str(self.path), "--version", "1.0.1", *extra
                )
                self.assertEqual(status, 1)
                self.assertIn("is read-only", err)
        self.assertEqual(self.path.read_bytes(), before)
        status, out, _ = self.run_tool(
            "set", str(self.path), "--version", "1.0.0"
        )
        self.assertEqual(status, 0)
        self.assertIn("no change", out)

    @unittest.skipIf(sys.platform == "win32", "POSIX directory permissions")
    @unittest.skipIf(
        hasattr(os, "geteuid") and os.geteuid() == 0,
        "root ignores file permissions",
    )
    def test_read_only_directory_is_refused(self) -> None:
        before = self.path.read_bytes()
        self.path.parent.chmod(0o555)
        self.addCleanup(self.path.parent.chmod, 0o755)
        status, _, err = self.run_tool(
            "set", str(self.path), "--version", "1.0.1"
        )
        self.assertEqual(status, 1)
        self.assertIn("directory", err)
        self.assertIn("read-only", err)
        self.assertEqual(self.path.read_bytes(), before)

    def test_external_data_stays_external(self) -> None:
        import onnx
        from onnx import TensorProto, helper

        model = onnx.load(str(self.path))
        weights = helper.make_tensor(
            "w",
            TensorProto.FLOAT,
            [256],
            struct.pack("<256f", *[0.5] * 256),
            raw=True,
        )
        model.graph.initializer.append(weights)
        path = self.path.with_name("external.onnx")
        onnx.save_model(
            model,
            str(path),
            save_as_external_data=True,
            all_tensors_to_one_file=True,
            location="external.data",
            size_threshold=0,
        )
        data_path = path.with_name("external.data")
        data_before = data_path.read_bytes()
        size_before = path.stat().st_size

        status, _, _ = self.run_tool("set", str(path), "--version", "1.0.1")

        self.assertEqual(status, 0)
        self.assertEqual(data_path.read_bytes(), data_before)
        self.assertLess(path.stat().st_size, size_before + 100)
        reloaded = onnx.load(str(path), load_external_data=False)
        self.assertEqual(
            reloaded.graph.initializer[0].data_location, TensorProto.EXTERNAL
        )

    @unittest.skipIf(sys.platform == "win32", "POSIX permission bits")
    def test_file_mode_is_kept(self) -> None:
        self.path.chmod(0o640)
        status, _, _ = self.run_tool(
            "set", str(self.path), "--version", "1.0.1"
        )
        self.assertEqual(status, 0)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o640)

    def test_symbolic_link_is_kept(self) -> None:
        real_dir = self.path.parent / "real"
        real_dir.mkdir()
        target = real_dir / "tiny.onnx"
        target.write_bytes(self.path.read_bytes())
        link = self.path.parent / "link.onnx"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symbolic links are not available")

        status, _, _ = self.run_tool("set", str(link), "--version", "1.0.1")

        self.assertEqual(status, 0)
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), target.resolve())
        status, out, _ = self.run_tool("show", "--json", str(target))
        self.assertEqual(json.loads(out)[0]["model_version"], "1.0.1")
        self.assertEqual(
            sorted(p.name for p in real_dir.iterdir()), ["tiny.onnx"]
        )

    def test_set_needs_a_field(self) -> None:
        status, _, err = self.run_tool("set", str(self.path))
        self.assertEqual(status, 2)
        self.assertIn("at least one field", err)

    def test_usage_errors(self) -> None:
        for argv in ((), ("unknown",), ("set",)):
            with self.subTest(argv=argv):
                status, _, _ = self.run_tool(*argv)
                self.assertEqual(status, 2)


@skip_without_script
class MissingOnnxTestCase(unittest.TestCase):
    def run_main(self, error: ImportError, installed: bool) -> str:
        err = io.StringIO()
        found = object() if installed else None
        with contextlib.ExitStack() as stack:
            stack.enter_context(
                mock.patch.object(tool, "_load", side_effect=error)
            )
            stack.enter_context(
                mock.patch.object(
                    tool.importlib.util, "find_spec", return_value=found
                )
            )
            stack.enter_context(contextlib.redirect_stderr(err))
            self.assertEqual(tool.main(["show", "x.onnx"]), 1)
        return err.getvalue()

    def test_message_without_onnx(self) -> None:
        message = self.run_main(ImportError(), installed=False)
        self.assertIn("pip install onnx", message)

    def test_broken_onnx_shows_the_cause(self) -> None:
        message = self.run_main(ImportError("DLL load failed"), installed=True)
        self.assertIn("DLL load failed", message)
        self.assertNotIn("pip install", message)


@skip_without_script
class CorpusTestCase(unittest.TestCase):
    @unittest.skipUnless(HAS_ONNX, "the onnx package is not installed")
    def test_default_lists_bundled_models(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(tool.main(["show", "--json"]), 0)
        names = {
            Path(item["path"]).name for item in json.loads(out.getvalue())
        }
        self.assertTrue(
            {"deepcut.onnx", "thai2rom_encoder.onnx"} <= names, names
        )


if __name__ == "__main__":
    unittest.main()
