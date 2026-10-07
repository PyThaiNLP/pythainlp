# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for pythainlp.corpus.core internals.

Cover the download manager, the corpus path lookup, the version
constraint checker, and the safe archive extraction helpers.

The tests never touch the network or the real user data directory:
``urllib.request.urlopen`` is replaced by an in-memory fake, and
``PYTHAINLP_DATA`` points to a temporary directory.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import posixpath
import shutil
import stat
import sys
import tarfile
import tempfile
import types
import unittest
import warnings
import zipfile
from contextlib import ExitStack, redirect_stdout, suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Optional, Union
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from pythainlp.corpus import core, corpus_path
from pythainlp.tools.path import safe_path_join

_CATALOG_URL = "https://example.invalid/db.json"
_FILE_URL = "https://example.invalid/files/"

# (member name, kind, payload)
# kind: "file" (payload: bytes), "sym" or "lnk" (payload: link target),
# "fifo" or "dir" (payload: None)
_TarMember = tuple[str, str, Optional[Union[bytes, str]]]

# Absolute POSIX paths such as "/etc/passwd" have a different meaning
# on Windows. Tests that depend on them run on POSIX systems only.
_skip_on_windows = unittest.skipIf(
    os.name == "nt", "POSIX paths and symbolic links are not portable"
)


def _symlinks_supported() -> bool:
    """Tell whether the process can create a symbolic link."""
    with tempfile.TemporaryDirectory() as probe_dir:
        target = Path(probe_dir, "target")
        target.write_bytes(b"")
        try:
            os.symlink(target, Path(probe_dir, "link"))
        except (OSError, NotImplementedError):
            return False
    return True


def _tar_bytes(
    members: list[_TarMember], mode: Literal["w", "w:gz"] = "w"
) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode=mode) as tar:
        for name, kind, payload in members:
            info = tarfile.TarInfo(name)
            if kind == "file":
                data = payload if isinstance(payload, bytes) else b""
                info.size = len(data)
                tar.addfile(info, io.BytesIO(data))
                continue
            info.type = {
                "sym": tarfile.SYMTYPE,
                "lnk": tarfile.LNKTYPE,
                "fifo": tarfile.FIFOTYPE,
                "dir": tarfile.DIRTYPE,
            }[kind]
            if isinstance(payload, str):
                info.linkname = payload
            tar.addfile(info)
    return buf.getvalue()


def _zip_bytes(members: list[tuple[str, bytes, bool]]) -> bytes:
    """Build a zip archive. Each member is (name, data, is_symlink)."""
    buf = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # duplicate names
        with zipfile.ZipFile(buf, "w") as zf:
            for name, data, is_symlink in members:
                info = zipfile.ZipInfo(name)
                mode = (stat.S_IFLNK | 0o777) if is_symlink else 0o100644
                info.external_attr = mode << 16
                zf.writestr(info, data)
    return buf.getvalue()


def _md5(data: bytes) -> str:
    return hashlib.md5(data, usedforsecurity=False).hexdigest()


def _snapshot(root: Path) -> dict[str, bytes]:
    """Map each file below *root* to its content."""
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file()
    }


# Data directory with the archive and the corpus of make_old_folder()
_OLD_TREE = [
    "c.tar",
    "c_1.0",
    "c_1.0/keep.txt",
    "c_1.0/old",
    "c_1.0/old/a.txt",
]
_NEW_TREE_ZIP = ["c.zip", "c_1.0", "c_1.0/a.txt", "db.json"]
# Temporary file of a download of "c.txt"
_PART_FILE_RE = r"^\.c\.txt\.[0-9a-f]{32}\.part$"


def _tree(root: Path) -> list[str]:
    """List all paths below *root*, relative and sorted."""
    return sorted(
        p.relative_to(root).as_posix() for p in root.rglob("*") if p != root
    )


class _FakeResponse(io.BytesIO):
    """In-memory stand-in for :class:`http.client.HTTPResponse`."""

    def __init__(self, data: bytes, with_length: bool = True) -> None:
        super().__init__(data)
        self.status = 200
        self.headers: dict[str, str] = (
            {"Content-Length": str(len(data))} if with_length else {}
        )

    def info(self) -> dict[str, str]:
        return self.headers


class _BrokenResponse(_FakeResponse):
    """Fail with *error* after the first chunk is read."""

    def __init__(self, data: bytes, error: BaseException) -> None:
        super().__init__(data)
        self.error = error

    def read(self, size: Optional[int] = -1) -> bytes:
        if self.tell():
            raise self.error
        return super().read(size)


class _FakeNetwork:
    """Serve registered URLs from memory; record every request."""

    def __init__(self) -> None:
        self.routes: dict[str, Union[bytes, BaseException]] = {}
        self.requests: list[str] = []
        self.user_agents: list[Optional[str]] = []

    def urlopen(self, req: Any, timeout: float = 0) -> _FakeResponse:
        url = req.full_url
        self.requests.append(url)
        self.user_agents.append(req.get_header("User-agent"))
        route = self.routes.get(url)
        if route is None:
            raise URLError(f"no route to {url}")
        if isinstance(route, BaseException):
            raise route
        return _FakeResponse(route)


def _no_network(req: Any, timeout: float = 0) -> None:
    raise AssertionError(f"unexpected network access: {req.full_url}")


class _IsolatedDataDirTestCase(unittest.TestCase):
    """Run each test with a temporary data directory and no network."""

    def setUp(self) -> None:
        self.data_dir = Path(tempfile.mkdtemp(prefix="pythainlp-test-"))
        self.addCleanup(shutil.rmtree, self.data_dir, ignore_errors=True)
        env = {
            k: v
            for k, v in os.environ.items()
            if k
            not in (
                "PYTHAINLP_DATA_DIR",
                "PYTHAINLP_OFFLINE",
                "PYTHAINLP_READ_MODE",
                "PYTHAINLP_READ_ONLY",
            )
        }
        env["PYTHAINLP_DATA"] = str(self.data_dir)
        self.db_path = str(self.data_dir / "db.json")
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.dict(os.environ, env, clear=True))
        stack.enter_context(
            patch.object(core, "corpus_db_path", return_value=self.db_path)
        )
        stack.enter_context(patch("urllib.request.urlopen", _no_network))
        # Make the progress bar import fail, so "Done." is printed.
        stack.enter_context(patch.dict(sys.modules, {"tqdm.auto": None}))
        self.stack = stack

    def read_db(self) -> Any:
        with open(self.db_path, encoding="utf-8") as f:
            return json.load(f)

    def write_db(self, db: Any, encoding: str = "utf-8") -> None:
        with open(self.db_path, "w", encoding=encoding) as f:
            json.dump(db, f)


# Golden data recorded from the code before the refactor.
# Rows: (pythainlp version, one outcome per cause in _CV_CAUSES).
# Outcome: "T" True, "F" False, "E" ValueError from parsing "x".
_CV_CAUSES = (
    "*",
    "==5.4.0",
    "==5.4",
    "==5.4.0<6",
    "==5.4.0>1",
    ">=5.4.0",
    ">=5.4.1",
    ">5.3.9",
    ">5.4.0",
    ">=5.0<5.4.0",
    ">=5.0<6.0",
    ">=5.0<=5.4.0",
    ">=5.4.1<=6",
    ">5.0<6.0",
    ">5.4.0<6.0",
    "<=5.4.0",
    "<=5.3.99",
    "<6.0",
    "<5.4.0",
    "",
    "~=5.4",
    ">>5.0",
    ">=9<x",
    ">=1<x",
    "<=x",
    "abc",
    ">=5.0-rc1",
    "==5.*",
    "<=5.4.*",
    ">=5.4.0<6.0<7",
    ">=9.0.0<x",
    ">9.0.0<x",
    ">=9.0.0<=x",
    ">=9",
    "<x",
    ">=>=5.0",
    "==5.4.0==",
)
_CV_ERROR = ("ValueError", "invalid literal for int() with base 10: 'x00'")
_CV_ROWS = (
    ("5.4.0", "TTTFFTFTFFTTFTFTFTFFFTEEEFTFTTFFFTETT"),
    ("5.4.0dev1", "TTTFFTFTFFTTFTFTFTFFFTEEEFTFTTFFFTETT"),
    ("5.4.0beta2", "TTTFFTFTFFTTFTFTFTFFFTEEEFTFTTFFFTETT"),
    ("5.3.10", "TFFFFFFTFTTTFTFTTTTFFTEEEFTFTFFFFTETF"),
    ("6.0", "TFFFFTTTTFFFFFFFFFFFFTEEEFTFFFFFFTETF"),
)
_CV_CODES = {"T": True, "F": False, "E": _CV_ERROR}


def _outcome(func: Any, *args: Any, **kwargs: Any) -> Any:
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return (type(e).__name__, str(e))


class CheckVersionTestCase(unittest.TestCase):
    def test_golden(self) -> None:
        for version, expected in _CV_ROWS:
            with patch.object(core, "__version__", version):
                self.assertEqual(len(expected), len(_CV_CAUSES))
                for cause, code in zip(_CV_CAUSES, expected):
                    with self.subTest(version=version, cause=cause):
                        self.assertEqual(
                            _outcome(core._check_version, cause),
                            _CV_CODES[code],
                        )

    def test_range_upper_bound_not_parsed_when_lower_fails(self) -> None:
        # Chained comparison short-circuits: the bad upper bound is
        # never parsed when the lower bound already fails.
        with patch.object(core, "__version__", "5.4.0"):
            self.assertFalse(core._check_version(">=9.0.0<x"))
            with self.assertRaises(ValueError):
                core._check_version(">=1.0.0<x")

    def test_current_version_parse_error_raises_for_any_cause(self) -> None:
        # The installed version is parsed before the cause is looked at.
        with patch.object(core, "__version__", "not.a.version"):
            with self.assertRaises(ValueError):
                core._check_version("*")

    def test_single_component_version_bug(self) -> None:
        # BUG-LEDGER: version2int-single-component
        # "9" becomes 900 instead of 90000, so ">=9" accepts 5.4.0.
        self.assertEqual(core._version2int("9"), 900)
        with patch.object(core, "__version__", "5.4.0"):
            self.assertTrue(core._check_version(">=9"))


# Archives that both tar branches accept: (members, extracted tree)
_TAR_ACCEPTED: tuple[tuple[list[_TarMember], list[str]], ...] = (
    ([], []),
    ([("a.txt", "file", b"a")], ["a.txt"]),
    ([("d", "dir", None), ("d/a.txt", "file", b"a")], ["d", "d/a.txt"]),
    ([("a.txt", "file", b"1"), ("a.txt", "file", b"2")], ["a.txt"]),
)

# Archives with links that stay inside: (members, extracted tree).
# The "data" filter accepts them; the manual branch rejects every link.
_TAR_INSIDE_LINKS: tuple[tuple[list[_TarMember], list[str]], ...] = (
    ([("link", "sym", "a.txt")], ["link"]),
    ([("sub/link", "sym", "../a.txt")], ["sub", "sub/link"]),
    (
        [("a.txt", "file", b"a"), ("hard", "lnk", "a.txt")],
        ["a.txt", "hard"],
    ),
    # A hard link target is relative to the archive root
    (
        [("sub/a.txt", "file", b"a"), ("sub/hard", "lnk", "sub/a.txt")],
        ["sub", "sub/a.txt", "sub/hard"],
    ),
    # A symlink chain that stays inside
    (
        [("d", "dir", None), ("b", "sym", "d"), ("a", "sym", "b/x")],
        ["a", "b", "d"],
    ),
)

# Archives that both tar branches reject:
# (members, message without data_filter, error type name with data_filter)
_TAR_REJECTED: tuple[tuple[list[_TarMember], str, str], ...] = (
    (
        [("../evil.txt", "file", b"x")],
        "Attempted path traversal in tar file: ../evil.txt",
        "OutsideDestinationError",
    ),
    (
        [("a/../../evil.txt", "file", b"x")],
        "Attempted path traversal in tar file: a/../../evil.txt",
        "OutsideDestinationError",
    ),
    (
        [("ok.txt", "file", b"x"), ("../evil.txt", "file", b"x")],
        "Attempted path traversal in tar file: ../evil.txt",
        "OutsideDestinationError",
    ),
    (
        [("link", "sym", "../../etc/passwd")],
        "Link in tar file: link",
        "LinkOutsideDestinationError",
    ),
    (
        [("sub/link", "sym", "../../evil")],
        "Link in tar file: sub/link",
        "LinkOutsideDestinationError",
    ),
    (
        [("hard", "lnk", "../outside")],
        "Link in tar file: hard",
        "LinkOutsideDestinationError",
    ),
    (
        [("sub/hard", "lnk", "../x")],
        "Link in tar file: sub/hard",
        "LinkOutsideDestinationError",
    ),
    (
        [("pipe", "fifo", None)],
        "Special file in tar file: pipe",
        "SpecialFileError",
    ),
)

# Symlink chains: "b" -> "." makes "b/../x" escape on a file system.
# (members, message without data_filter). Older "data" filters reject
# them; newer ones normalize the names lexically, so they stay inside.
_TAR_CHAINS: tuple[tuple[list[_TarMember], str], ...] = (
    ([("b", "sym", "."), ("a", "sym", "b/../x")], "Link in tar file: b"),
    (
        [("d", "sym", "."), ("d/../evil.txt", "file", b"x")],
        "Link in tar file: d",
    ),
    ([("d", "sym", "."), ("h", "lnk", "d/../x")], "Link in tar file: d"),
)

# Absolute POSIX link targets, rejected by both tar branches
_TAR_REJECTED_POSIX: tuple[tuple[list[_TarMember], str, str], ...] = (
    (
        [("link", "sym", "/etc/passwd")],
        "Link in tar file: link",
        "AbsoluteLinkError",
    ),
    (
        [("hard", "lnk", "/etc/passwd")],
        "Link in tar file: hard",
        "AbsoluteLinkError",
    ),
    (
        [("link", "sym", "/../../x")],
        "Link in tar file: link",
        "AbsoluteLinkError",
    ),
)


def _late_binding_members() -> list[_TarMember]:
    """
    Return a symlink that escapes only after a later link exists.

    "a" -> "d1/d2/x/../.." is inside while "x" is missing. Once
    "d1/d2/x" -> "../.." is extracted, "a" points to the parent of the
    destination.
    """
    return [
        ("a", "sym", "d1/d2/x/../.."),
        ("d1", "dir", None),
        ("d1/d2", "dir", None),
        ("d1/d2/x", "sym", "../.."),
        ("a/evil.txt", "file", b"x"),
    ]


def _path_max_members() -> list[_TarMember]:
    """
    Return a CVE-2025-4517 style archive.

    Short symlinks to long directory names make the resolved path longer
    than PATH_MAX, so an unpatched ``os.path.realpath`` stops resolving
    and checks a wrong path. Then "escape" points two levels above the
    destination and "escape/evil.txt" is written there.
    """
    long_name = "d" * (55 if sys.platform == "darwin" else 247)
    steps = "abcdefghijklmnop"
    members: list[_TarMember] = []
    path = ""
    for step in steps:
        members.append((posixpath.join(path, long_name), "dir", None))
        members.append((posixpath.join(path, step), "sym", long_name))
        path = posixpath.join(path, long_name)
    link_path = posixpath.join(*steps, "l" * 254)
    members.append((link_path, "sym", "../" * len(steps)))
    members.append(("escape", "sym", link_path + "/../.."))
    members.append(("escape/evil.txt", "file", b"x"))
    return members


if TYPE_CHECKING:
    _MixinBase = unittest.TestCase
else:
    _MixinBase = object


class _SafeExtractTarTestMixin(_MixinBase):
    """
    Tests shared by both ``_safe_extract_tar`` branches.

    Archives are extracted for real into a temporary directory.
    """

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="pythainlp-tar-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        if not _symlinks_supported():
            self.skipTest("cannot create symbolic links")
        self.dest = self.root / "dest"
        self.dest.mkdir()

    def extract(self, members: list[_TarMember]) -> None:
        self.extract_archive(_tar_bytes(members))

    def extract_archive(self, data: bytes) -> None:
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            core._safe_extract_tar(tar, str(self.dest))

    def reset_dest(self) -> None:
        shutil.rmtree(self.dest)
        self.dest.mkdir()

    def assert_nothing_outside(self) -> None:
        self.assertEqual(
            [p.name for p in self.root.iterdir()], ["dest"], "escaped dest"
        )

    def check_error(
        self, error: ValueError, message: str, error_type: str
    ) -> None:
        raise NotImplementedError

    def check_rejected(
        self, cases: tuple[tuple[list[_TarMember], str, str], ...]
    ) -> None:
        for members, message, error_type in cases:
            with self.subTest(members=members):
                self.reset_dest()
                with self.assertRaises(ValueError) as ctx:
                    self.extract(members)
                self.check_error(ctx.exception, message, error_type)
                self.assert_nothing_outside()

    def test_accepts(self) -> None:
        for members, tree in _TAR_ACCEPTED:
            with self.subTest(members=members):
                self.reset_dest()
                self.extract(members)
                self.assertEqual(_tree(self.dest), tree)
                self.assert_nothing_outside()

    def test_duplicate_members_last_wins(self) -> None:
        self.extract([("a.txt", "file", b"1"), ("a.txt", "file", b"2")])
        self.assertEqual((self.dest / "a.txt").read_bytes(), b"2")

    def test_rejects(self) -> None:
        self.check_rejected(_TAR_REJECTED)

    @_skip_on_windows
    def test_rejects_absolute_link(self) -> None:
        self.check_rejected(_TAR_REJECTED_POSIX)

    def assert_links_inside(self) -> None:
        real_dest = os.path.realpath(self.dest)
        for link in self.dest.rglob("*"):
            if link.is_symlink():
                target = os.path.realpath(link)
                self.assertEqual(
                    os.path.commonpath([target, real_dest]),
                    real_dest,
                    f"{link} -> {target}",
                )

    @_skip_on_windows
    def test_symlink_chains_stay_inside(self) -> None:
        for members, _ in _TAR_CHAINS:
            with self.subTest(members=members):
                self.reset_dest()
                # KeyError: a newer "data" filter normalizes the hard
                # link target to "x", which is not in the archive.
                with suppress(ValueError, KeyError):
                    self.extract(members)
                self.assert_nothing_outside()
                self.assert_links_inside()

    @_skip_on_windows
    def test_late_binding_symlink_stays_inside(self) -> None:
        # Rejected by the manual branch. A patched "data" filter
        # normalizes the target of "a" to "d1".
        with suppress(ValueError):
            self.extract(_late_binding_members())
        self.assert_nothing_outside()
        self.assert_links_inside()

    @_skip_on_windows
    def test_path_max_bypass_rejected(self) -> None:
        self.dest = self.root / "x" / "dest"
        self.dest.mkdir(parents=True)
        try:
            self.extract(_path_max_members())
        except (ValueError, OSError):
            pass  # OSError: name too long on a patched Python
        else:
            self.fail("archive accepted")
        self.assertFalse((self.root / "evil.txt").exists())
        self.assertFalse((self.root / "x" / "evil.txt").exists())

    @_skip_on_windows
    def test_file_mode_is_limited(self) -> None:
        # (mode in archive, mode on disk), as with tarfile.data_filter
        cases = ((0o4777, 0o755), (0o666, 0o644), (0o640, 0o640), (0, 0o600))
        for mode, expected in cases:
            with self.subTest(mode=oct(mode)):
                self.reset_dest()
                info = tarfile.TarInfo("a.txt")
                info.mode = mode
                buf = io.BytesIO()
                with tarfile.open(fileobj=buf, mode="w") as tar:
                    tar.addfile(info, io.BytesIO(b""))
                self.extract_archive(buf.getvalue())
                actual = (self.dest / "a.txt").stat().st_mode & 0o7777
                self.assertEqual(oct(actual), oct(expected))


class SafeExtractTarDataFilterTestCase(
    _SafeExtractTarTestMixin, unittest.TestCase
):
    """
    Branch that uses the "data" extraction filter of ``tarfile``.

    The filter exists in Python 3.12 and later, and in the security
    releases 3.9.17, 3.10.12, and 3.11.4.
    """

    def setUp(self) -> None:
        if not hasattr(tarfile, "data_filter"):
            self.skipTest("tarfile.data_filter is not available")
        # os.path.ALLOW_MISSING came with the 2025 fixes of the filter
        # (CVE-2025-4517). Older filters can be escaped.
        if not hasattr(os.path, "ALLOW_MISSING") and self._testMethodName in (
            "test_late_binding_symlink_stays_inside",
            "test_path_max_bypass_rejected",
        ):
            self.skipTest("tarfile.data_filter without the 2025 fixes")
        super().setUp()

    def check_error(
        self, error: ValueError, message: str, error_type: str
    ) -> None:
        # Every tarfile.FilterError becomes a ValueError
        self.assertEqual(type(error.__cause__).__name__, error_type)
        self.assertEqual(str(error), str(error.__cause__))

    def test_accepts_inside_links(self) -> None:
        for members, tree in _TAR_INSIDE_LINKS:
            with self.subTest(members=members):
                self.reset_dest()
                self.extract(members)
                self.assertEqual(_tree(self.dest), tree)
                self.assert_nothing_outside()

    def test_links_work(self) -> None:
        self.extract(
            [
                ("dir", "dir", None),
                ("dir/a.txt", "file", b"a"),
                ("link", "sym", "dir/a.txt"),
                ("dir/hard", "lnk", "dir/a.txt"),
            ]
        )
        self.assertEqual((self.dest / "link").read_bytes(), b"a")
        self.assertEqual((self.dest / "dir" / "hard").read_bytes(), b"a")

    @_skip_on_windows
    def test_absolute_member_is_kept_inside(self) -> None:
        self.extract([("/abs/evil.txt", "file", b"x")])
        self.assertEqual((self.dest / "abs" / "evil.txt").read_bytes(), b"x")
        self.assert_nothing_outside()

    def test_other_errors_propagate(self) -> None:
        tar = MagicMock()
        tar.extractall.side_effect = OSError("disk full")
        with self.assertRaises(OSError):
            core._safe_extract_tar(tar, str(self.dest))


def _tarfile_without_data_filter() -> types.ModuleType:
    """Return a stand-in for the tarfile module of Python < 3.12."""
    proxy = types.ModuleType("tarfile")
    proxy.__dict__.update(
        {k: v for k, v in vars(tarfile).items() if k != "data_filter"}
    )
    return proxy


class SafeExtractTarManualTestCase(
    _SafeExtractTarTestMixin, unittest.TestCase
):
    """
    Branch without the "data" extraction filter: manual validation.

    ``TarFile.extractall`` runs without a filter, as in old Python.
    """

    def setUp(self) -> None:
        super().setUp()
        patcher = patch.object(core, "tarfile", _tarfile_without_data_filter())
        patcher.start()
        self.addCleanup(patcher.stop)
        self.extractall_calls: list[Any] = []

    def extract_archive(self, data: bytes) -> None:
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            original = tar.extractall
            # Python with extraction filters needs "fully_trusted" to
            # behave like Python without them.
            kwargs: dict[str, Any] = (
                {"filter": "fully_trusted"}
                if hasattr(tarfile, "fully_trusted_filter")
                else {}
            )

            def legacy_extractall(
                path: str, members: Optional[Any] = None
            ) -> None:
                original(path=path, members=members, **kwargs)

            with patch.object(
                tar, "extractall", side_effect=legacy_extractall
            ) as extractall:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", DeprecationWarning)
                    try:
                        core._safe_extract_tar(tar, str(self.dest))
                    finally:
                        self.extractall_calls = extractall.call_args_list

    def check_error(
        self, error: ValueError, message: str, error_type: str
    ) -> None:
        self.assertEqual(str(error), message)
        self.assertIsNone(error.__cause__)

    def test_errors_extract_nothing(self) -> None:
        # Names and types are checked before extraction
        cases = [m for m, _, _ in _TAR_REJECTED] + [m for m, _ in _TAR_CHAINS]
        cases += [_late_binding_members(), _path_max_members()]
        for members in cases:
            with self.subTest(members=members[:2]):
                self.reset_dest()
                with self.assertRaises(ValueError):
                    self.extract(members)
                self.assertEqual(self.extractall_calls, [])
                self.assertEqual(_tree(self.dest), [])

    def test_rejects_all_links(self) -> None:
        for members, _ in _TAR_INSIDE_LINKS:
            first_link = next(m[0] for m in members if m[1] in ("sym", "lnk"))
            with self.subTest(members=members):
                self.reset_dest()
                with self.assertRaises(ValueError) as ctx:
                    self.extract(members)
                self.assertEqual(
                    str(ctx.exception), f"Link in tar file: {first_link}"
                )
                self.assertEqual(_tree(self.dest), [])

    def test_rejects_symlink_chains(self) -> None:
        for members, message in _TAR_CHAINS:
            with self.subTest(members=members):
                self.reset_dest()
                with self.assertRaises(ValueError) as ctx:
                    self.extract(members)
                self.assertEqual(str(ctx.exception), message)

    def test_late_binding_symlink_message(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.extract(_late_binding_members())
        self.assertEqual(str(ctx.exception), "Link in tar file: a")

    @_skip_on_windows
    def test_path_max_bypass_rejected_by_type(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.extract(_path_max_members())
        self.assertEqual(str(ctx.exception), "Link in tar file: a")
        self.assertEqual(_tree(self.dest), [])

    @_skip_on_windows
    def test_absolute_member_name_rejected(self) -> None:
        # tarfile strips a leading "/" when reading, so set it directly
        info = tarfile.TarInfo("x")
        info.name = "/etc/evil"
        tar = MagicMock()
        tar.getmembers.return_value = [info]
        with self.assertRaises(ValueError) as ctx:
            core._safe_extract_tar(tar, str(self.dest))
        self.assertEqual(
            str(ctx.exception),
            "Attempted path traversal in tar file: /etc/evil",
        )
        tar.extractall.assert_not_called()

    def test_member_check_accepts_inner_dot_dot(self) -> None:
        # Not extracted for real: tarfile of Python 3.9 cannot create
        # the parent "a/.." of "a/../b.txt".
        core._check_tar_member(str(self.dest), tarfile.TarInfo("a/../b.txt"))

    def test_directory_mode(self) -> None:
        for mode, expected in ((0o777, 0o755), (0o555, 0o755), (0, 0o700)):
            with self.subTest(mode=oct(mode)):
                info = tarfile.TarInfo("d")
                info.type = tarfile.DIRTYPE
                info.mode = mode
                self.assertEqual(core._data_filter_mode(info), expected)

    def test_owner_is_dropped(self) -> None:
        info = tarfile.TarInfo("a.txt")
        info.uid, info.gid, info.uname, info.gname = 0, 0, "root", "wheel"
        tar = MagicMock()
        tar.getmembers.return_value = [info]
        core._safe_extract_tar(tar, str(self.dest))
        (members,) = [c.kwargs["members"] for c in tar.extractall.mock_calls]
        self.assertEqual(
            [(m.uid, m.gid, m.uname, m.gname) for m in members],
            [(-1, -1, "", "")],
        )
        # The archive member itself is not changed
        self.assertEqual((info.uid, info.uname), (0, "root"))

    @_skip_on_windows
    def test_owner_is_not_restored_as_root(self) -> None:
        # As root, tarfile calls os.chown(); -1 keeps the current owner
        info = tarfile.TarInfo("a.txt")
        info.uid, info.gid, info.uname, info.gname = 1234, 5678, "x", "y"
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tar:
            tar.addfile(info, io.BytesIO(b""))
            tar.addfile(_dir_info("d", 4321))
        members = [("a.txt",), ("d",)]
        with patch("os.geteuid", return_value=0, create=True):
            with patch("os.chown") as chown:
                buf.seek(0)
                with tarfile.open(fileobj=buf) as tar:
                    original = tar.extractall
                    kwargs: dict[str, Any] = (
                        {"filter": "fully_trusted"}
                        if hasattr(tarfile, "fully_trusted_filter")
                        else {}
                    )
                    with patch.object(
                        tar,
                        "extractall",
                        side_effect=lambda path, members=None: original(
                            path=path, members=members, **kwargs
                        ),
                    ):
                        core._safe_extract_tar(tar, str(self.dest))
        self.assertEqual(len(chown.call_args_list), len(members))
        for call in chown.call_args_list:
            self.assertEqual(call.args[1:], (-1, -1))


def _dir_info(name: str, uid: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type = tarfile.DIRTYPE
    info.uid = info.gid = uid
    info.uname = info.gname = "root"
    return info


class SafeExtractZipTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="pythainlp-zip-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.dest = self.root / "dest"
        self.dest.mkdir()

    def extract(self, members: list[tuple[str, bytes, bool]]) -> None:
        with zipfile.ZipFile(io.BytesIO(_zip_bytes(members))) as zf:
            core._safe_extract_zip(zf, str(self.dest))

    def assert_nothing_outside(self) -> None:
        self.assertEqual([p.name for p in self.root.iterdir()], ["dest"])

    def test_accepts(self) -> None:
        cases: list[tuple[list[tuple[str, bytes, bool]], list[str]]] = [
            ([], []),
            ([("a.txt", b"a", False)], ["a.txt"]),
            ([("d/a.txt", b"a", False)], ["d", "d/a.txt"]),
            # zipfile drops ".." components instead of resolving them
            ([("a/../b.txt", b"b", False)], ["a", "a/b.txt"]),
            ([("link", b"a.txt", True)], ["link"]),
            ([("d/link", b"../a.txt", True)], ["d", "d/link"]),
            ([("a.txt", b"1", False), ("a.txt", b"2", False)], ["a.txt"]),
        ]
        for members, tree in cases:
            with self.subTest(members=members):
                shutil.rmtree(self.dest)
                self.dest.mkdir()
                self.extract(members)
                self.assertEqual(_tree(self.dest), tree)
                self.assert_nothing_outside()

    @_skip_on_windows
    def test_accepts_posix_specific(self) -> None:
        # zipfile does not convert a backslash on POSIX systems.
        self.extract([("..\\evil.txt", b"x", False)])
        self.assertEqual(_tree(self.dest), ["..\\evil.txt"])
        self.assert_nothing_outside()

    def test_symlink_is_written_as_regular_file(self) -> None:
        self.extract([("link", b"a.txt", True)])
        link = self.dest / "link"
        self.assertFalse(link.is_symlink())
        self.assertEqual(link.read_bytes(), b"a.txt")

    def test_rejects(self) -> None:
        cases: list[tuple[list[tuple[str, bytes, bool]], str]] = [
            (
                [("../evil.txt", b"x", False)],
                "Attempted path traversal in zip file: ../evil.txt",
            ),
            (
                [("a/../../evil.txt", b"x", False)],
                "Attempted path traversal in zip file: a/../../evil.txt",
            ),
            (
                [("ok.txt", b"x", False), ("../evil.txt", b"x", False)],
                "Attempted path traversal in zip file: ../evil.txt",
            ),
            (
                [("link", b"../x", True)],
                "Symlink link points outside extraction directory: ../x",
            ),
            (
                [("d/link", b"../../x", True)],
                "Symlink d/link points outside extraction directory: ../../x",
            ),
            # Absolute targets are rejected, as in tar
            (
                [("link", b"/etc/passwd", True)],
                (
                    "Symlink link points outside extraction directory: "
                    "/etc/passwd"
                ),
            ),
            (
                [("link", b"/../../x", True)],
                "Symlink link points outside extraction directory: /../../x",
            ),
            # Each entry is checked, even under a duplicate name
            (
                [("link", b"../../x", True), ("link", b"data", False)],
                "Symlink link points outside extraction directory: ../../x",
            ),
        ]
        if os.name != "nt":
            cases.append(
                (
                    [("/etc/evil", b"x", False)],
                    "Attempted path traversal in zip file: /etc/evil",
                )
            )
        for members, message in cases:
            with self.subTest(members=members):
                with self.assertRaises(ValueError) as ctx:
                    self.extract(members)
                self.assertEqual(str(ctx.exception), message)
                self.assertIsNone(ctx.exception.__cause__)
                self.assertEqual(_tree(self.dest), [])
                self.assert_nothing_outside()

    def test_non_utf8_symlink_target(self) -> None:
        with self.assertRaises(UnicodeDecodeError):
            self.extract([("link", b"\xff\xfe", True)])
        self.assertEqual(_tree(self.dest), [])


def _catalog_entry(
    name: str, versions: dict[str, dict[str, str]]
) -> dict[str, Any]:
    return {"name": name, "versions": versions}


def _version_entry(
    filename: str,
    data: bytes,
    pythainlp_version: str = "*",
    is_tar_gz: str = "False",
    is_zip: str = "False",
    md5: Optional[str] = None,
) -> dict[str, str]:
    return {
        "filename": filename,
        "download_url": _FILE_URL + filename,
        "md5": _md5(data) if md5 is None else md5,
        "is_tar_gz": is_tar_gz,
        "is_zip": is_zip,
        "pythainlp_version": pythainlp_version,
    }


class _DownloadTestBase(_IsolatedDataDirTestCase):
    """Serve a corpus catalog and files from an in-memory network."""

    def setUp(self) -> None:
        super().setUp()
        self.net = _FakeNetwork()
        self.stack.enter_context(
            patch("urllib.request.urlopen", self.net.urlopen)
        )
        self.catalog: dict[str, Any] = {}

    def serve(self, filename: str, data: bytes) -> None:
        self.net.routes[_FILE_URL + filename] = data

    def run_download(self, *args: Any, **kwargs: Any) -> tuple[Any, str]:
        self.net.routes.setdefault(
            _CATALOG_URL, json.dumps(self.catalog).encode("utf-8")
        )
        kwargs.setdefault("url", _CATALOG_URL)
        out = io.StringIO()
        with redirect_stdout(out):
            result = _outcome(core.download, *args, **kwargs)
        return result, out.getvalue()


class DownloadTestCase(_DownloadTestBase):
    def test_read_only(self) -> None:
        with patch.dict(os.environ, {"PYTHAINLP_READ_ONLY": "1"}):
            result, out = self.run_download("x")
        self.assertIs(result, False)
        self.assertEqual(
            out, "PyThaiNLP is in read-only mode. It cannot download.\n"
        )
        self.assertEqual(self.net.requests, [])

    def test_default_catalog_url(self) -> None:
        self.net.routes[_CATALOG_URL] = b"{}"
        with patch.object(core, "corpus_db_url", return_value=_CATALOG_URL):
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertFalse(core.download("x"))
        self.assertEqual(self.net.requests, [_CATALOG_URL])
        self.assertEqual(out.getvalue(), "Corpus not found: x\n")
        ua = self.net.user_agents[0]
        self.assertIsNotNone(ua)
        self.assertTrue(str(ua).startswith("PyThaiNLP/"))

    def test_catalog_unavailable(self) -> None:
        self.net.routes[_CATALOG_URL] = HTTPError(
            _CATALOG_URL,
            404,
            "Not Found",
            None,  # type: ignore[arg-type]
            None,
        )
        result, out = self.run_download("x")
        self.assertIs(result, False)
        self.assertEqual(
            out,
            "HTTP error occurred: HTTP Error 404: Not Found\n"
            f"Cannot download corpus catalog from: {_CATALOG_URL}\n",
        )

    def test_catalog_invalid_json(self) -> None:
        self.net.routes[_CATALOG_URL] = b"not json"
        result, out = self.run_download("x")
        self.assertEqual(result[0], "ValueError")
        self.assertTrue(result[1].startswith("Failed to parse JSON response"))
        self.assertEqual(out, "")

    def test_name_not_in_catalog(self) -> None:
        result, out = self.run_download("x")
        self.assertIs(result, False)
        self.assertEqual(out, "Corpus not found: x\n")
        self.assertFalse(os.path.exists(self.db_path))

    def test_no_supported_version(self) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"", "<0.0.1")}
        )
        result, out = self.run_download("c")
        self.assertIs(result, False)
        self.assertEqual(out, "Corpus: c\nCorpus not found.\n")
        self.assertFalse(os.path.exists(self.db_path))

    def test_explicit_version_missing(self) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"")}
        )
        result, out = self.run_download("c", version="0.2")
        self.assertIs(result, False)
        self.assertEqual(out, "Corpus: c\nCorpus not found.\n")

    def test_explicit_version_not_supported(self) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"", "<0.0.1")}
        )
        result, out = self.run_download("c", version="0.1")
        self.assertIs(result, False)
        self.assertEqual(out, "Corpus: c\nCorpus version not supported.\n")

    def test_last_matching_version_wins(self) -> None:
        # BUG-LEDGER: download-last-version
        # The last compatible version in catalog order is chosen,
        # not the highest one.
        self.catalog["c"] = _catalog_entry(
            "c",
            {
                "0.2": _version_entry("c2.txt", b"2"),
                "0.3": _version_entry("c3.txt", b"3", "<0.0.1"),
                "0.1": _version_entry("c1.txt", b"1"),
            },
        )
        self.serve("c1.txt", b"1")
        result, out = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(out, "Corpus: c\n- Downloading: c 0.1\nDone.\n")
        self.assertEqual(self.read_db()["_default"]["1"]["version"], "0.1")

    def test_fresh_download_creates_db(self) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"hello")}
        )
        self.serve("c.txt", b"hello")
        self.assertFalse(os.path.exists(self.db_path))
        result, out = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(out, "Corpus: c\n- Downloading: c 0.1\nDone.\n")
        self.assertEqual((self.data_dir / "c.txt").read_bytes(), b"hello")
        self.assertEqual(
            self.read_db(),
            {
                "_default": {
                    "1": {
                        "name": "c",
                        "version": "0.1",
                        "filename": "c.txt",
                        "is_folder": False,
                        "foldername": None,
                    }
                }
            },
        )
        self.assertEqual(
            self.net.requests, [_CATALOG_URL, _FILE_URL + "c.txt"]
        )

    def test_skip_hash_check(self) -> None:
        for md5 in ("", "-"):
            with self.subTest(md5=md5):
                self.catalog["c"] = _catalog_entry(
                    "c", {"0.1": _version_entry("c.txt", b"x", md5=md5)}
                )
                self.net.routes.pop(_CATALOG_URL, None)
                self.serve("c.txt", b"other")
                result, _ = self.run_download("c", force=True)
                self.assertIs(result, True)

    def test_hash_mismatch(self) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"expected")}
        )
        self.serve("c.txt", b"tampered")
        result, out = self.run_download("c")
        self.assertEqual(
            result, ("ValueError", "Hash does not match expected.")
        )
        self.assertEqual(out, "Corpus: c\n- Downloading: c 0.1\nDone.\n")
        self.assertFalse(os.path.exists(self.db_path))
        # The downloaded file is removed
        self.assertEqual(_tree(self.data_dir), [])

    def test_hash_mismatch_remove_fails(self) -> None:
        # The hash error is raised even if the temporary file cannot be
        # removed. The file is never moved into place.
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"expected")}
        )
        self.serve("c.txt", b"tampered")
        with patch("os.remove", side_effect=OSError("busy")):
            result, _ = self.run_download("c")
        self.assertEqual(
            result, ("ValueError", "Hash does not match expected.")
        )
        (leftover,) = _tree(self.data_dir)
        self.assertRegex(leftover, _PART_FILE_RE)

    def test_file_download_fails(self) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        result, _ = self.run_download("c")
        self.assertEqual(result[0], "URLError")
        self.assertFalse(os.path.exists(self.db_path))

    def test_traversal_filename_rejected(self) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("../evil.txt", b"x")}
        )
        self.serve("../evil.txt", b"x")
        result, _ = self.run_download("c")
        self.assertEqual(result[0], "ValueError")
        self.assertIn("Path traversal attempt detected", result[1])
        self.assertFalse((self.data_dir.parent / "evil.txt").exists())
        self.assertFalse(os.path.exists(self.db_path))

    def test_already_up_to_date(self) -> None:
        self.write_db(
            {
                "_default": {
                    "3": {"name": "c", "version": "0.1", "filename": "c.txt"}
                }
            },
            encoding="utf-8-sig",
        )
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        result, out = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(out, "Corpus: c\n- Already up to date.\n")
        self.assertEqual(self.net.requests, [_CATALOG_URL])

    def test_other_version_installed(self) -> None:
        self.write_db(
            {
                "_default": {
                    "1": {"name": "c", "version": "0.0", "filename": "c.txt"}
                }
            }
        )
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        result, out = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(
            out,
            "Corpus: c\n"
            "- Existing version: 0.0\n"
            "- New version available: 0.1\n"
            "- Use download(data_name, force=True) to update\n",
        )

    def test_force_updates_existing_entry(self) -> None:
        self.write_db(
            {
                "_default": {
                    "1": {"name": "a", "version": "1", "filename": "a"},
                    "2": {
                        "name": "c",
                        "version": "0.0",
                        "filename": "old.txt",
                        "extra": 1,
                    },
                }
            }
        )
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        self.serve("c.txt", b"x")
        result, _ = self.run_download("c", force=True)
        self.assertIs(result, True)
        self.assertEqual(
            self.read_db()["_default"],
            {
                "1": {"name": "a", "version": "1", "filename": "a"},
                "2": {
                    "name": "c",
                    "version": "0.1",
                    "filename": "c.txt",
                    "extra": 1,
                    "is_folder": False,
                    "foldername": None,
                },
            },
        )

    def test_new_entry_gets_next_number(self) -> None:
        self.write_db(
            {
                "_default": {
                    "1": {"name": "a"},
                    "10": {"name": "b"},
                    "2": {"name": "d"},
                }
            }
        )
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        self.serve("c.txt", b"x")
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(
            list(self.read_db()["_default"]), ["1", "10", "2", "11"]
        )

    def test_tar_gz_archive(self) -> None:
        data = _tar_bytes([("m/a.txt", "file", b"a")], mode="w:gz")
        self.catalog["c"] = _catalog_entry(
            "c", {"1.0": _version_entry("c.tar.gz", data, is_tar_gz="True")}
        )
        self.serve("c.tar.gz", data)
        result, out = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(
            (self.data_dir / "c_1.0" / "m" / "a.txt").read_bytes(), b"a"
        )
        entry = self.read_db()["_default"]["1"]
        self.assertEqual(entry["is_folder"], True)
        self.assertEqual(entry["foldername"], "c_1.0")
        self.assertEqual(entry["filename"], "c.tar.gz")

    def test_zip_archive_replaces_existing_folder(self) -> None:
        data = _zip_bytes([("a.txt", b"a", False)])
        self.catalog["c"] = _catalog_entry(
            "c", {"1.0": _version_entry("c.zip", data, is_zip="True")}
        )
        self.serve("c.zip", data)
        (self.data_dir / "c_1.0").mkdir()
        (self.data_dir / "c_1.0" / "a.txt").write_bytes(b"old")
        (self.data_dir / "c_1.0" / "stale").write_bytes(b"s")
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(_tree(self.data_dir / "c_1.0"), ["a.txt"])
        self.assertEqual(
            (self.data_dir / "c_1.0" / "a.txt").read_bytes(), b"a"
        )
        self.assertEqual(_tree(self.data_dir), _NEW_TREE_ZIP)
        entry = self.read_db()["_default"]["1"]
        self.assertEqual(
            (entry["is_folder"], entry["foldername"]), (True, "c_1.0")
        )

    def test_tar_takes_precedence_over_zip(self) -> None:
        data = _tar_bytes([("a.txt", "file", b"a")])
        self.catalog["c"] = _catalog_entry(
            "c",
            {
                "1.0": _version_entry(
                    "c.tar", data, is_tar_gz="True", is_zip="True"
                )
            },
        )
        self.serve("c.tar", data)
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        self.assertTrue((self.data_dir / "c_1.0" / "a.txt").exists())

    def test_malicious_archives_rejected(self) -> None:
        archives = {
            "tar": (
                _tar_bytes([("../../evil.txt", "file", b"x")]),
                {"is_tar_gz": "True"},
            ),
            "zip": (
                _zip_bytes([("../../evil.txt", b"x", False)]),
                {"is_zip": "True"},
            ),
        }
        for kind, (data, flags) in archives.items():
            with self.subTest(kind=kind):
                filename = f"c.{kind}"
                self.catalog["c"] = _catalog_entry(
                    "c", {"1.0": _version_entry(filename, data, **flags)}
                )
                self.net.routes.pop(_CATALOG_URL, None)
                self.serve(filename, data)
                result, _ = self.run_download("c")
                self.assertEqual(result[0], "ValueError")
                self.assertFalse((self.data_dir.parent / "evil.txt").exists())
                self.assertFalse(os.path.exists(self.db_path))
                # The extraction folder is removed; the archive stays
                self.assertEqual(_tree(self.data_dir), [filename])
                (self.data_dir / filename).unlink()

    def serve_tar(self) -> None:
        data = _tar_bytes([("a.txt", "file", b"a")])
        self.catalog["c"] = _catalog_entry(
            "c", {"1.0": _version_entry("c.tar", data, is_tar_gz="True")}
        )
        self.serve("c.tar", data)

    def test_failed_extraction_removes_new_folder(self) -> None:
        def partial_extract(tar: Any, path: str) -> None:
            Path(path, "new.txt").write_bytes(b"n")
            Path(path, "sub").mkdir()
            Path(path, "sub", "x").write_bytes(b"x")
            raise ValueError("rejected")

        self.serve_tar()
        with patch.object(core, "_safe_extract_tar", partial_extract):
            result, _ = self.run_download("c")
        self.assertEqual(result, ("ValueError", "rejected"))
        self.assertEqual(_tree(self.data_dir), ["c.tar"])
        self.assertFalse(os.path.exists(self.db_path))

    def make_old_folder(self) -> dict[str, bytes]:
        """Create an installed corpus folder; return its snapshot."""
        folder = self.data_dir / "c_1.0"
        (folder / "old").mkdir(parents=True)
        (folder / "old" / "a.txt").write_bytes(b"old")
        (folder / "keep.txt").write_bytes(b"k")
        return _snapshot(folder)

    def test_failed_extraction_keeps_existing_folder(self) -> None:
        snapshot = self.make_old_folder()
        paths: list[str] = []

        def partial_extract(tar: Any, path: str) -> None:
            paths.append(path)
            Path(path, "new.txt").write_bytes(b"n")
            Path(path, "old").mkdir()
            Path(path, "old", "a.txt").write_bytes(b"new")
            raise KeyboardInterrupt

        self.serve_tar()
        with patch.object(core, "_safe_extract_tar", partial_extract):
            with self.assertRaises(KeyboardInterrupt):
                self.run_download("c")
        # Extracted into a temporary folder next to the corpus folder
        self.assertEqual(
            Path(paths[0]).parent.resolve(), self.data_dir.resolve()
        )
        self.assertRegex(Path(paths[0]).name, r"^\.c_1\.0\.[0-9a-f]{32}\.tmp$")
        self.assertEqual(_snapshot(self.data_dir / "c_1.0"), snapshot)
        self.assertEqual(_tree(self.data_dir), _OLD_TREE)

    def test_forced_reextraction_failure_keeps_old_folder(self) -> None:
        # A real archive that fails part way, on both tar branches
        snapshot = self.make_old_folder()
        data = _tar_bytes(
            [
                ("old/a.txt", "file", b"new"),
                ("new.txt", "file", b"n"),
                ("pipe", "fifo", None),
            ]
        )
        self.catalog["c"] = _catalog_entry(
            "c", {"1.0": _version_entry("c.tar", data, is_tar_gz="True")}
        )
        self.serve("c.tar", data)
        for module in (tarfile, _tarfile_without_data_filter()):
            with self.subTest(manual=module is not tarfile):
                self.net.routes.pop(_CATALOG_URL, None)
                with patch.object(core, "tarfile", module):
                    result, _ = self.run_download("c", force=True)
                self.assertEqual(result[0], "ValueError")
                self.assertEqual(_snapshot(self.data_dir / "c_1.0"), snapshot)
                self.assertEqual(_tree(self.data_dir), _OLD_TREE)

    def test_concurrent_install_finishes_first(self) -> None:
        # Another process installs the folder while this one extracts.
        # The complete new folder replaces it; the old one is removed.
        folder = self.data_dir / "c_1.0"

        def other_process_extract(tar: Any, path: str) -> None:
            folder.mkdir()
            (folder / "other.txt").write_bytes(b"o")
            Path(path, "a.txt").write_bytes(b"a")

        self.serve_tar()
        with patch.object(core, "_safe_extract_tar", other_process_extract):
            result, _ = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(_snapshot(folder), {"a.txt": b"a"})
        self.assertEqual(
            _tree(self.data_dir), ["c.tar", "c_1.0", "c_1.0/a.txt", "db.json"]
        )

    def test_concurrent_install_kept_when_extraction_fails(self) -> None:
        # A failed extraction never removes a folder it did not create
        folder = self.data_dir / "c_1.0"

        def other_process_extract(tar: Any, path: str) -> None:
            folder.mkdir()
            (folder / "other.txt").write_bytes(b"o")
            raise ValueError("rejected")

        self.serve_tar()
        with patch.object(core, "_safe_extract_tar", other_process_extract):
            result, _ = self.run_download("c")
        self.assertEqual(result, ("ValueError", "rejected"))
        self.assertEqual(_snapshot(folder), {"other.txt": b"o"})
        self.assertEqual(
            _tree(self.data_dir), ["c.tar", "c_1.0", "c_1.0/other.txt"]
        )

    def test_failed_swap_restores_old_folder(self) -> None:
        snapshot = self.make_old_folder()
        real_rename = os.rename
        calls: list[tuple[str, str]] = []

        def rename(src: str, dst: str) -> None:
            calls.append((src, dst))
            if len(calls) == 2:  # moving the new folder into place
                raise OSError("busy")
            real_rename(src, dst)

        self.serve_tar()
        with patch("os.rename", side_effect=rename):
            result, _ = self.run_download("c", force=True)
        self.assertEqual(result, ("OSError", "busy"))
        self.assertEqual(len(calls), 3)
        self.assertEqual(_snapshot(self.data_dir / "c_1.0"), snapshot)
        self.assertEqual(_tree(self.data_dir), _OLD_TREE)

    def test_failed_rollback_raises_first_error(self) -> None:
        # The old folder cannot be moved back: it stays hidden, and the
        # error of the first move is raised, not that of the rollback
        snapshot = self.make_old_folder()
        new_path = self.data_dir / "new"
        new_path.mkdir()
        real_rename = os.rename
        calls: list[tuple[str, str]] = []
        busy = OSError("busy")

        def rename(src: str, dst: str) -> None:
            calls.append((src, dst))
            if len(calls) == 2:
                raise busy
            if len(calls) == 3:
                raise OSError("locked")
            real_rename(src, dst)

        folder = str(self.data_dir / "c_1.0")
        with patch("os.rename", side_effect=rename):
            with self.assertRaises(OSError) as ctx:
                core._swap_in_folder(str(new_path), folder)
        self.assertIs(ctx.exception, busy)
        old_path = calls[0][1]
        self.assertEqual(calls[2], (old_path, folder))
        self.assertRegex(Path(old_path).name, r"^\.c_1\.0\.[0-9a-f]{32}\.old$")
        self.assertEqual(_snapshot(Path(old_path)), snapshot)
        self.assertFalse(os.path.exists(folder))
        if sys.version_info >= (3, 11):
            self.assertEqual(
                busy.__notes__, [f"The old folder is kept at: {old_path}"]
            )

    def test_add_note_without_note_support_warns(self) -> None:
        class NoNotes(Exception):
            add_note = None

        error = NoNotes()
        with self.assertWarns(RuntimeWarning) as cm:
            core._add_note(error, "note")
        self.assertEqual(str(cm.warning), "note")
        self.assertFalse(hasattr(error, "__notes__"))

    def test_symlinked_folder_is_replaced_not_followed(self) -> None:
        if not _symlinks_supported():
            self.skipTest("cannot create symbolic links")
        outside = Path(tempfile.mkdtemp(prefix="pythainlp-outside-"))
        self.addCleanup(shutil.rmtree, outside, ignore_errors=True)
        (outside / "precious.txt").write_bytes(b"p")
        os.symlink(outside, self.data_dir / "c_1.0")
        self.serve_tar()
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        self.assertFalse((self.data_dir / "c_1.0").is_symlink())
        self.assertEqual(_snapshot(self.data_dir / "c_1.0"), {"a.txt": b"a"})
        self.assertEqual(_snapshot(outside), {"precious.txt": b"p"})

    def test_failed_extraction_does_not_follow_new_symlink(self) -> None:
        if not _symlinks_supported():
            self.skipTest("cannot create symbolic links")
        outside = Path(tempfile.mkdtemp(prefix="pythainlp-outside-"))
        self.addCleanup(shutil.rmtree, outside, ignore_errors=True)
        (outside / "precious.txt").write_bytes(b"p")
        folder = self.data_dir / "c_1.0"
        folder.mkdir()

        def partial_extract(tar: Any, path: str) -> None:
            os.symlink(outside, Path(path, "link"))
            raise ValueError("rejected")

        self.serve_tar()
        with patch.object(core, "_safe_extract_tar", partial_extract):
            result, _ = self.run_download("c")
        self.assertEqual(result, ("ValueError", "rejected"))
        self.assertEqual(_tree(folder), [])
        self.assertEqual((outside / "precious.txt").read_bytes(), b"p")

    def test_symlink_chain_does_not_escape(self) -> None:
        # Rejected and cleaned up, or kept inside by a newer "data" filter
        if not _symlinks_supported():
            self.skipTest("cannot create symbolic links")
        data = _tar_bytes(
            [
                ("a.txt", "file", b"a"),
                ("d", "sym", "."),
                ("d/../evil.txt", "file", b"x"),
            ]
        )
        self.catalog["c"] = _catalog_entry(
            "c", {"1.0": _version_entry("c.tar", data, is_tar_gz="True")}
        )
        self.serve("c.tar", data)
        branches = {"data_filter": tarfile}
        branches["manual"] = _tarfile_without_data_filter()
        for branch, module in branches.items():
            with self.subTest(branch=branch):
                self.net.routes.pop(_CATALOG_URL, None)
                # The archive stays; an installed folder is kept
                before = sorted({*_tree(self.data_dir), "c.tar"})
                with patch.object(core, "tarfile", module):
                    with warnings.catch_warnings():
                        # Python 3.12 and 3.13 warn about no filter
                        warnings.simplefilter("ignore", DeprecationWarning)
                        result, _ = self.run_download("c", force=True)
                # "d/../evil.txt" would land in the data directory
                self.assertFalse((self.data_dir / "evil.txt").exists())
                if result is not True:
                    self.assertEqual(result[0], "ValueError")
                    self.assertEqual(_tree(self.data_dir), before)

    def test_progress_bar(self) -> None:
        bars: list[MagicMock] = []

        def fake_tqdm(total: int) -> MagicMock:
            bar = MagicMock()
            bar.total = total
            bars.append(bar)
            return bar

        tqdm_auto = types.ModuleType("tqdm.auto")
        setattr(tqdm_auto, "tqdm", fake_tqdm)
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x" * 70000)}
        )
        self.serve("c.txt", b"x" * 70000)
        with patch.dict(sys.modules, {"tqdm.auto": tqdm_auto}):
            result, out = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(out, "Corpus: c\n- Downloading: c 0.1\n")
        self.assertEqual(len(bars), 1)
        self.assertEqual(bars[0].total, 70000)
        self.assertEqual(
            [c.args for c in bars[0].update.call_args_list],
            [(65536,), (4464,)],
        )
        bars[0].close.assert_called_once_with()

    def test_missing_content_length(self) -> None:
        def urlopen(req: Any, timeout: float = 0) -> _FakeResponse:
            if req.full_url == _CATALOG_URL:
                return _FakeResponse(json.dumps(self.catalog).encode())
            return _FakeResponse(b"x", with_length=False)

        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        with patch("urllib.request.urlopen", urlopen):
            with redirect_stdout(io.StringIO()):
                size = core._download(_FILE_URL + "c.txt", "c.txt")
        self.assertEqual(size, -1)

    def test_downloads_into_temporary_file(self) -> None:
        (self.data_dir / "c.txt").write_bytes(b"old")
        moves: list[tuple[str, str]] = []
        real_replace = core._replace_file

        def replace_file(src: str, dst: str) -> None:
            moves.append((src, dst))
            self.assertEqual(Path(src).read_bytes(), b"new")
            self.assertEqual(Path(dst).read_bytes(), b"old")
            real_replace(src, dst)

        with patch(
            "urllib.request.urlopen", return_value=_FakeResponse(b"new")
        ):
            with patch.object(core, "_replace_file", replace_file):
                with redirect_stdout(io.StringIO()):
                    size = core._download(
                        _FILE_URL + "c.txt", "c.txt", _md5(b"new")
                    )
        self.assertEqual(size, 3)
        ((src, dst),) = moves
        self.assertEqual(Path(src).parent.resolve(), self.data_dir.resolve())
        self.assertRegex(Path(src).name, _PART_FILE_RE)
        self.assertEqual(
            Path(dst).resolve(), (self.data_dir / "c.txt").resolve()
        )
        self.assertEqual(_snapshot(self.data_dir), {"c.txt": b"new"})

    def test_failed_download_keeps_existing_file(self) -> None:
        # A failed or interrupted download leaves no temporary file
        # behind and keeps a file that existed before, byte for byte
        failures: list[tuple[str, Any, str]] = [
            ("KeyboardInterrupt", KeyboardInterrupt(), ""),
            ("OSError", OSError("reset"), ""),
            ("mismatch", None, _md5(b"other")),
        ]
        for existing in ({}, {"c.txt": b"old"}):
            for label, error, md5 in failures:
                with self.subTest(existing=bool(existing), failure=label):
                    for name, data in existing.items():
                        (self.data_dir / name).write_bytes(data)
                    response: _FakeResponse = (
                        _FakeResponse(b"x" * 70000)
                        if error is None
                        else _BrokenResponse(b"x" * 70000, error)
                    )
                    with patch(
                        "urllib.request.urlopen", return_value=response
                    ):
                        with redirect_stdout(io.StringIO()):
                            with self.assertRaises(
                                ValueError if error is None else type(error)
                            ):
                                core._download(
                                    _FILE_URL + "c.txt", "c.txt", md5
                                )
                    self.assertEqual(_snapshot(self.data_dir), existing)
                    self.assertEqual(_tree(self.data_dir), list(existing))

    def test_failed_replace_keeps_existing_path(self) -> None:
        # A directory in the way cannot be replaced; it is not removed
        (self.data_dir / "c.txt").mkdir()
        with patch("urllib.request.urlopen", return_value=_FakeResponse(b"x")):
            with redirect_stdout(io.StringIO()):
                with self.assertRaises(OSError):
                    core._download(_FILE_URL + "c.txt", "c.txt")
        self.assertEqual(_tree(self.data_dir), ["c.txt"])

    def test_empty_key_in_local_db(self) -> None:
        # An entry under key "" is found like any other entry
        self.write_db({"_default": {"": {"name": "c", "version": "0.1"}}})
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        self.serve("c.txt", b"x")
        result, out = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(out, "Corpus: c\n- Already up to date.\n")

        result, _ = self.run_download("c", force=True)
        self.assertIs(result, True)
        self.assertEqual(
            self.read_db()["_default"],
            {
                "": {
                    "name": "c",
                    "version": "0.1",
                    "filename": "c.txt",
                    "is_folder": False,
                    "foldername": None,
                }
            },
        )

    def test_new_entry_number_ignores_non_numeric_keys(self) -> None:
        cases = (
            ({"": {"name": "a"}}, "1"),
            ({"": {"name": "a"}, "x": {"name": "b"}, "2": {"name": "d"}}, "3"),
            ({"²": {"name": "a"}, "-5": {"name": "b"}}, "1"),
        )
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        self.serve("c.txt", b"x")
        for entries, key in cases:
            with self.subTest(entries=entries):
                self.write_db({"_default": dict(entries)})
                result, _ = self.run_download("c")
                self.assertIs(result, True)
                db_entries = self.read_db()["_default"]
                self.assertEqual(list(db_entries), [*entries, key])
                self.assertEqual(db_entries[key]["name"], "c")


class FailedDownloadTestCase(_DownloadTestBase):
    """A failed download keeps the corpus removable."""

    def publish(self, filename: str, data: bytes, **kwargs: str) -> None:
        self.catalog["c"] = _catalog_entry(
            "c", {"1.0": _version_entry(filename, data, **kwargs)}
        )
        self.net.routes[_CATALOG_URL] = json.dumps(self.catalog).encode()
        self.serve(filename, data)

    def break_download(self, mode: str, filename: str) -> None:
        """Make the next download of *filename* fail in *mode*."""
        if mode == "mismatch":
            self.serve(filename, b"tampered")
            return
        real = self.net.urlopen

        def urlopen(req: Any, timeout: float = 0) -> _FakeResponse:
            if req.full_url == _FILE_URL + filename:
                return _BrokenResponse(b"x" * 70000, OSError("reset"))
            return real(req, timeout=timeout)

        self.stack.enter_context(patch("urllib.request.urlopen", urlopen))

    def check_failed_forced_download(
        self, mode: str, filename: str, data: bytes, **kwargs: str
    ) -> None:
        self.publish(filename, data, **kwargs)
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        before = _snapshot(self.data_dir)
        self.assertEqual(before[filename], data)
        self.break_download(mode, filename)
        result, _ = self.run_download("c", force=True)
        self.assertEqual(
            result[0], "ValueError" if mode == "mismatch" else "OSError"
        )
        # The file of the earlier download stays on disk, unchanged,
        # and so does its extracted folder
        self.assertEqual(_snapshot(self.data_dir), before)
        n_requests = len(self.net.requests)
        self.assertIs(core.remove("c"), True)
        self.assertEqual(len(self.net.requests), n_requests)
        self.assertEqual(_tree(self.data_dir), ["db.json"])
        self.assertEqual(self.read_db()["_default"], {})

    def check_fresh_failed_download(self, mode: str) -> None:
        self.publish("c.txt", b"content")
        self.break_download(mode, "c.txt")
        result, _ = self.run_download("c")
        self.assertEqual(
            result[0], "ValueError" if mode == "mismatch" else "OSError"
        )
        self.assertEqual(_tree(self.data_dir), [])

    def test_remove_after_forced_mismatch_folder(self) -> None:
        data = _zip_bytes([("a.txt", b"a", False)])
        self.check_failed_forced_download(
            "mismatch", "c.zip", data, is_zip="True"
        )

    def test_remove_after_forced_network_error_folder(self) -> None:
        data = _zip_bytes([("a.txt", b"a", False)])
        self.check_failed_forced_download(
            "network", "c.zip", data, is_zip="True"
        )

    def test_remove_after_forced_mismatch_file(self) -> None:
        self.check_failed_forced_download("mismatch", "c.txt", b"content")

    def test_remove_after_forced_network_error_file(self) -> None:
        self.check_failed_forced_download("network", "c.txt", b"content")

    def test_fresh_mismatch_leaves_no_file(self) -> None:
        self.check_fresh_failed_download("mismatch")

    def test_fresh_network_error_leaves_no_file(self) -> None:
        self.check_fresh_failed_download("network")

    def test_remove_missing_file_does_not_download(self) -> None:
        self.publish("c.txt", b"content")
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        (self.data_dir / "c.txt").unlink()
        n_requests = len(self.net.requests)
        self.assertIs(core.remove("c"), True)
        self.assertEqual(len(self.net.requests), n_requests)
        self.assertEqual(self.read_db()["_default"], {})

    def test_forced_download_keeps_mode_and_symlink(self) -> None:
        if not _symlinks_supported() or os.name == "nt":
            self.skipTest("needs symbolic links and POSIX modes")
        self.publish("c.txt", b"new")
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        target = self.data_dir / "target.bin"
        target.write_bytes(b"old")
        target.chmod(0o600)
        link = self.data_dir / "c.txt"
        link.unlink()
        link.symlink_to(target)
        result, _ = self.run_download("c", force=True)
        self.assertIs(result, True)
        self.assertTrue(link.is_symlink())
        self.assertEqual(target.read_bytes(), b"new")
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)

    def test_remove_tolerates_missing_archive(self) -> None:
        data = _zip_bytes([("a.txt", b"a", False)])
        self.publish("c.zip", data, is_zip="True")
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        (self.data_dir / "c.zip").unlink()
        self.assertIs(core.remove("c"), True)
        self.assertEqual(_tree(self.data_dir), ["db.json"])


class LocalDbWriteTestCase(_DownloadTestBase):
    """Writes of the local catalog (``db.json``) are atomic."""

    def setUp(self) -> None:
        super().setUp()
        self.catalog["c"] = _catalog_entry(
            "c", {"0.1": _version_entry("c.txt", b"x")}
        )
        self.serve("c.txt", b"x")
        self.old_db = {"_default": {"1": {"name": "a", "version": "1"}}}
        self.write_db(self.old_db)

    def test_no_temporary_file_left(self) -> None:
        result, _ = self.run_download("c")
        self.assertIs(result, True)
        self.assertEqual(_tree(self.data_dir), ["c.txt", "db.json"])
        self.assertEqual(list(self.read_db()["_default"]), ["1", "2"])

    def test_failed_write_keeps_old_catalog(self) -> None:
        for target in ("json.dump", "os.replace"):
            with self.subTest(target=target):
                self.net.routes.pop(_CATALOG_URL, None)
                with patch(target, side_effect=OSError("full")):
                    result, _ = self.run_download("c", force=True)
                self.assertEqual(result, ("OSError", "full"))
                self.assertEqual(self.read_db(), self.old_db)
                self.assertEqual(_tree(self.data_dir), ["c.txt", "db.json"])

    def test_interrupted_write_keeps_old_catalog(self) -> None:
        with patch("os.fsync", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.run_download("c")
        self.assertEqual(self.read_db(), self.old_db)
        self.assertEqual(_tree(self.data_dir), ["c.txt", "db.json"])

    def test_remove_writes_atomically(self) -> None:
        self.write_db(
            {
                "_default": {
                    "1": {"name": "a", "version": "1", "filename": "a.txt"},
                    "2": {"name": "c", "version": "1", "filename": "c.txt"},
                }
            }
        )
        (self.data_dir / "c.txt").write_bytes(b"x")
        self.assertIs(core.remove("c"), True)
        self.assertEqual(_tree(self.data_dir), ["db.json"])
        self.assertEqual(list(self.read_db()["_default"]), ["1"])

    @_skip_on_windows
    def test_permission_bits_are_kept(self) -> None:
        for mode in (0o600, 0o640, 0o664):
            with self.subTest(mode=oct(mode)):
                os.chmod(self.db_path, mode)
                core._write_local_db(self.old_db)
                self.assertEqual(
                    oct(stat.S_IMODE(os.stat(self.db_path).st_mode)), oct(mode)
                )

    def test_symlinked_catalog_target_is_replaced(self) -> None:
        if not _symlinks_supported():
            self.skipTest("cannot create symbolic links")
        shared_dir = Path(tempfile.mkdtemp(prefix="pythainlp-shared-"))
        self.addCleanup(shutil.rmtree, shared_dir, ignore_errors=True)
        shared = shared_dir / "db.json"
        os.replace(self.db_path, shared)
        os.symlink(shared, self.db_path)
        new_db = {"_default": {"2": {"name": "b"}}}
        core._write_local_db(new_db)
        self.assertTrue(os.path.islink(self.db_path))
        self.assertEqual(json.loads(shared.read_text("utf-8")), new_db)
        self.assertEqual(self.read_db(), new_db)
        self.assertEqual(_tree(shared_dir), ["db.json"])
        self.assertEqual(_tree(self.data_dir), ["db.json"])

    def test_replace_retries_permission_error(self) -> None:
        new_db = {"_default": {"2": {"name": "b"}}}
        real_replace = os.replace
        errors = [PermissionError("in use")] * 2

        def replace(src: str, dst: str) -> None:
            if errors:
                raise errors.pop()
            real_replace(src, dst)

        with patch.object(core, "_REPLACE_RETRIES", 5):
            with patch("os.replace", side_effect=replace) as replace_mock:
                with patch("time.sleep") as sleep:
                    core._write_local_db(new_db)
        self.assertEqual(replace_mock.call_count, 3)
        self.assertEqual(sleep.call_count, 2)
        sleep.assert_called_with(0.05)
        self.assertEqual(self.read_db(), new_db)
        self.assertEqual(_tree(self.data_dir), ["db.json"])

    def test_replace_gives_up_after_retries(self) -> None:
        for retries in (0, 5):
            with self.subTest(retries=retries):
                with patch.object(core, "_REPLACE_RETRIES", retries):
                    with patch(
                        "os.replace", side_effect=PermissionError("in use")
                    ) as replace_mock:
                        with patch("time.sleep") as sleep:
                            with self.assertRaises(PermissionError):
                                core._write_local_db({"_default": {}})
                self.assertEqual(replace_mock.call_count, retries + 1)
                self.assertEqual(sleep.call_count, retries)
                self.assertEqual(self.read_db(), self.old_db)
                self.assertEqual(_tree(self.data_dir), ["db.json"])

    def test_read_only_mode_does_not_create_catalog(self) -> None:
        os.remove(self.db_path)
        with patch.dict(os.environ, {"PYTHAINLP_READ_ONLY": "1"}):
            self.assertIs(core.remove("c"), False)
            result, _ = self.run_download("c")
        self.assertIs(result, False)
        self.assertEqual(_tree(self.data_dir), [])


class GetCorpusPathTestCase(_IsolatedDataDirTestCase):
    def register(self, entry: dict[str, Any]) -> None:
        self.write_db({"_default": {"1": entry}})

    def test_bundled_corpus(self) -> None:
        expected = safe_path_join(corpus_path(), "deepcut.onnx")
        self.assertEqual(core.get_corpus_path("deepcut_onnx"), expected)
        self.assertEqual(
            core.get_corpus_path("deepcut_onnx", version="1.0.0"), expected
        )

    def test_registered_file(self) -> None:
        self.register({"name": "c", "version": "0.1", "filename": "c.txt"})
        (self.data_dir / "c.txt").write_bytes(b"x")
        self.assertEqual(
            core.get_corpus_path("c"), str(self.data_dir / "c.txt")
        )
        self.assertEqual(
            core.get_corpus_path("c", version="0.1"),
            str(self.data_dir / "c.txt"),
        )

    def test_registered_folder(self) -> None:
        self.register(
            {
                "name": "c",
                "version": "0.1",
                "filename": "c.zip",
                "is_folder": True,
                "foldername": "c_0.1",
            }
        )
        (self.data_dir / "c_0.1").mkdir()
        self.assertEqual(
            core.get_corpus_path("c"), str(self.data_dir / "c_0.1")
        )

    def test_registered_without_path_info(self) -> None:
        for entry in (
            {"name": "c", "version": "0.1"},
            {"name": "c", "version": "0.1", "filename": ""},
            {
                "name": "c",
                "version": "0.1",
                "is_folder": True,
                "filename": "f",
            },
        ):
            with self.subTest(entry=entry):
                self.register(entry)
                with patch.object(core, "download") as download:
                    self.assertIsNone(core.get_corpus_path("c"))
                download.assert_not_called()

    def test_not_registered_offline(self) -> None:
        with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": "1"}):
            with patch.object(core, "download") as download:
                with self.assertRaises(FileNotFoundError) as ctx:
                    core.get_corpus_path("c")
        download.assert_not_called()
        self.assertEqual(
            str(ctx.exception),
            "corpus-not-found name='c'\n"
            "  Corpus 'c' not found locally.\n"
            "  PYTHAINLP_OFFLINE is set; automatic downloading is disabled.\n"
            "  To download, unset PYTHAINLP_OFFLINE, then run:\n"
            "    Python: pythainlp.corpus.download('c')\n"
            "    CLI:    thainlp data get c",
        )

    def test_not_registered_download_fails(self) -> None:
        with patch.object(core, "download", return_value=False) as download:
            self.assertIsNone(core.get_corpus_path("c", version="0.2"))
        download.assert_called_once_with("c", version="0.2")

    def test_not_registered_download_without_entry(self) -> None:
        with patch.object(core, "download", return_value=True) as download:
            self.assertIsNone(core.get_corpus_path("c"))
        download.assert_called_once_with("c", version="")

    def test_not_registered_download_succeeds(self) -> None:
        def fake_download(name: str, version: str = "") -> bool:
            self.register(
                {"name": name, "version": "0.1", "filename": "c.txt"}
            )
            (self.data_dir / "c.txt").write_bytes(b"x")
            return True

        with patch.object(core, "download", side_effect=fake_download):
            self.assertEqual(
                core.get_corpus_path("c"), str(self.data_dir / "c.txt")
            )

    def test_not_registered_download_succeeds_file_missing(self) -> None:
        def fake_download(
            name: str, version: str = "", force: bool = False
        ) -> bool:
            self.register(
                {"name": name, "version": "0.1", "filename": "c.txt"}
            )
            return True

        with patch.object(
            core, "download", side_effect=fake_download
        ) as download:
            self.assertIsNone(core.get_corpus_path("c"))
        self.assertEqual(
            [c.kwargs for c in download.call_args_list],
            [{"version": ""}, {"version": "", "force": True}],
        )

    def test_registered_missing_offline(self) -> None:
        self.register({"name": "c", "version": "0.1", "filename": "c.txt"})
        path = str(self.data_dir / "c.txt")
        with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": "yes"}):
            with patch.object(core, "download") as download:
                with self.assertRaises(FileNotFoundError) as ctx:
                    core.get_corpus_path("c")
        download.assert_not_called()
        self.assertEqual(
            str(ctx.exception),
            f"corpus-not-found name='c' expected-path={path!r}\n"
            f"  Corpus 'c' expected at '{path}' but file not found.\n"
            "  PYTHAINLP_OFFLINE is set; automatic re-downloading is disabled.\n"
            "  To re-download, unset PYTHAINLP_OFFLINE, then run:\n"
            "    Python: pythainlp.corpus.download('c', force=True)\n"
            "    CLI:    thainlp data get c",
        )

    def test_registered_missing_redownload(self) -> None:
        self.register({"name": "c", "version": "0.1", "filename": "c.txt"})
        path = self.data_dir / "c.txt"

        def restore(name: str, version: str = "", force: bool = False) -> bool:
            path.write_bytes(b"x")
            return True

        cases = (
            (MagicMock(return_value=False), None),
            (MagicMock(return_value=True), None),
            (MagicMock(side_effect=restore), str(path)),
        )
        for download, expected in cases:
            with self.subTest(expected=expected):
                with patch.object(core, "download", download):
                    self.assertEqual(
                        core.get_corpus_path("c", version="0.1"), expected
                    )
                download.assert_called_once_with(
                    "c", version="0.1", force=True
                )

    def test_unknown_version_of_bundled_corpus_goes_to_catalog(self) -> None:
        with patch.object(core, "download", return_value=False) as download:
            self.assertIsNone(
                core.get_corpus_path("deepcut_onnx", version="9.9")
            )
        download.assert_called_once_with("deepcut_onnx", version="9.9")


if __name__ == "__main__":
    unittest.main()
