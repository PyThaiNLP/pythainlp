#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Comprehensive benchmark + cProfile evidence for Phase 1 Cython extensions.

Generates:
  1. Environment details
  2. Multi-scale comparison (small / medium / large)
  3. cProfile hotspot analysis (before / after)
  4. Dataset description

Usage:
    PYTHONPATH=. python3 scripts/bench_full_evidence.py
"""

import cProfile
import io
import platform
import pstats
import sys
import timeit
from collections.abc import Callable
from typing import Optional


# ---------------------------------------------------------------------------
# 1. Environment
# ---------------------------------------------------------------------------
def print_env() -> None:
    print("=" * 72)
    print("ENVIRONMENT")
    print("=" * 72)
    print(f"  OS            : {platform.system()} {platform.release()}")
    print(f"  Architecture  : {platform.machine()}")
    print(f"  CPU           : {_get_cpu_model()}")
    print(f"  Python        : {sys.version}")
    print(f"  pythainlp     : {_get_pythainlp_version()}")
    cython_ver = _get_cython_status()
    print(f"  Cython ext    : {cython_ver}")
    print()


def _get_cpu_model() -> str:
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        return platform.processor() or "unknown"
    return platform.processor() or "unknown"


def _get_pythainlp_version() -> str:
    try:
        import pythainlp

        return pythainlp.__version__
    except Exception:
        return "unknown"


def _get_cython_status() -> str:
    try:
        from pythainlp._ext import _thai_fast, _normalize_fast  # noqa: F401  # pyright: ignore[reportUnusedImport]

        return "loaded (compiled)"
    except ImportError:
        return "NOT available (pure Python mode)"


# ---------------------------------------------------------------------------
# 2. Dataset
# ---------------------------------------------------------------------------
# Thai Wikipedia-style sample text (real Thai prose)
_SAMPLE_SHORT = "สวัสดีครับ"  # 10 chars
_SAMPLE_MEDIUM = "ภาษาไทยเป็นภาษาที่มีวรรณยุกต์ ทำให้การออกเสียงมีความซับซ้อน" * 5  # ~310 chars
_SAMPLE_LONG = (
    "ประเทศไทยมีชื่อเรียกอย่างเป็นทางการว่า ราชอาณาจักรไทย "
    "เป็นรัฐที่ตั้งอยู่ในภูมิภาคเอเชียตะวันออกเฉียงใต้ "
    "มีพรมแดนทางทิศตะวันออกติดลาวและกัมพูชา ทิศใต้ติดอ่าวไทยและมาเลเซีย "
    "ทิศตะวันตกติดทะเลอันดามันและพม่า ทิศเหนือติดพม่าและลาว "
    "โดยมีแม่น้ำโขงกั้นเป็นบางช่วง "
) * 50  # ~6,000+ chars

_SAMPLE_HUGE = _SAMPLE_LONG * 10  # ~60,000+ chars

_TONE_SHORT = "คำว่า ต้น ไม้ แล้ว ก็ น้ำ"  # ~25 chars with tonemarks
_TONE_LONG = (
    "น้ำตกเจ็ดสาวน้อย เป็นน้ำตกที่สวยงามมาก ตั้งอยู่ในอุทยานแห่งชาติ "
    "เขื่อนศรีนครินทร์ จังหวัดกาญจนบุรี ล้อมรอบด้วยป่าดิบชื้น "
    "ต้นไม้ใหญ่ น้ำตกไหลจากหน้าผาสูง สร้างความชุ่มเย็นให้กับบริเวณรอบข้าง "
) * 40  # ~6,000+ chars


def print_dataset() -> None:
    print("=" * 72)
    print("DATASET")
    print("=" * 72)
    print("  Real Thai prose, constructed from Thai Wikipedia-style text.")
    print(f"  Short  : {len(_SAMPLE_SHORT):>8,} chars  (single greeting)")
    print(f"  Medium : {len(_SAMPLE_MEDIUM):>8,} chars  (paragraph)")
    print(f"  Long   : {len(_SAMPLE_LONG):>8,} chars  (article)")
    print(f"  Huge   : {len(_SAMPLE_HUGE):>8,} chars  (corpus batch)")
    print(f"  Tone-S : {len(_TONE_SHORT):>8,} chars  (short with tonemarks)")
    print(f"  Tone-L : {len(_TONE_LONG):>8,} chars  (long with tonemarks)")
    print()


# ---------------------------------------------------------------------------
# 3. Benchmark helpers
# ---------------------------------------------------------------------------
def bench(
    label: str,
    func_py: Callable[..., object],
    func_cy: Optional[Callable[..., object]],
    args: tuple,
    number: int = 50_000,
) -> dict:
    """Benchmark a single function, return result dict."""
    # Python
    timer_py = timeit.Timer(lambda: func_py(*args))
    times_py = timer_py.repeat(repeat=5, number=number)
    best_py = min(times_py)

    # Cython
    if func_cy is not None:
        timer_cy = timeit.Timer(lambda: func_cy(*args))
        times_cy = timer_cy.repeat(repeat=5, number=number)
        best_cy = min(times_cy)
        speedup = best_py / best_cy
    else:
        best_cy = None
        speedup = None

    return {
        "label": label,
        "py_time": best_py,
        "cy_time": best_cy,
        "speedup": speedup,
        "number": number,
    }


def print_table(title: str, rows: list[dict]) -> None:
    print(f"\n{'─' * 72}")
    print(f"  {title}")
    print(f"{'─' * 72}")
    print(
        f"  {'Function':<35} {'Python':>10} {'Cython':>10} {'Speedup':>10}"
    )
    print(f"  {'─' * 67}")
    for row in rows:
        cy_str = (
            f"{row['cy_time']:.4f}s" if row["cy_time"] is not None else "N/A"
        )
        sp_str = (
            f"{row['speedup']:.1f}x" if row["speedup"] is not None else "—"
        )
        print(
            f"  {row['label']:<35} {row['py_time']:>9.4f}s {cy_str:>10} {sp_str:>10}"
        )
    print()


# ---------------------------------------------------------------------------
# 4. cProfile analysis
# ---------------------------------------------------------------------------
def profile_function(
    func: Callable[..., object], args: tuple, repeat: int = 100_000
) -> str:
    """Profile a function with cProfile and return top-10 hotspots."""
    pr = cProfile.Profile()
    pr.enable()
    for _ in range(repeat):
        func(*args)
    pr.disable()

    stream = io.StringIO()
    ps = pstats.Stats(pr, stream=stream)
    ps.sort_stats("cumulative")
    ps.print_stats(15)
    return stream.getvalue()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print_env()
    print_dataset()

    # Import Python baselines
    from pythainlp.util.thai import (
        _py_count_thai,
        _py_is_thai,
        _py_is_thai_char,
    )
    from pythainlp.util.normalize import _py_remove_tonemark

    # Import Cython (may be None)
    try:
        from pythainlp._ext._thai_fast import (
            count_thai as cy_count_thai,
            is_thai as cy_is_thai,
            is_thai_char as cy_is_thai_char,
        )
        from pythainlp._ext._normalize_fast import (
            remove_tonemark as cy_remove_tonemark,
        )

        have_ext = True
    except ImportError:
        cy_is_thai_char = None
        cy_is_thai = None
        cy_count_thai = None
        cy_remove_tonemark = None
        have_ext = False

    if not have_ext:
        print("⚠  Cython extensions NOT available. Showing Python-only.\n")

    # ── Multi-Scale: is_thai_char ──────────────────────────────────────
    rows_itc = []
    rows_itc.append(
        bench(
            "is_thai_char (1M calls)",
            _py_is_thai_char,
            cy_is_thai_char,
            ("ก",),
            number=1_000_000,
        )
    )
    print_table("is_thai_char — Single Character Check", rows_itc)

    # ── Multi-Scale: is_thai ───────────────────────────────────────────
    rows_it = []
    for label, text, n in [
        ("is_thai (short, 10 ch)", _SAMPLE_SHORT, 500_000),
        ("is_thai (medium, ~310 ch)", _SAMPLE_MEDIUM, 100_000),
        ("is_thai (long, ~6K ch)", _SAMPLE_LONG, 10_000),
        ("is_thai (huge, ~60K ch)", _SAMPLE_HUGE, 1_000),
    ]:
        rows_it.append(bench(label, _py_is_thai, cy_is_thai, (text,), n))
    print_table("is_thai — Small-Scale vs Big-Scale", rows_it)

    # ── Multi-Scale: count_thai ────────────────────────────────────────
    rows_ct = []
    for label, text, n in [
        ("count_thai (short, 10 ch)", _SAMPLE_SHORT, 500_000),
        ("count_thai (medium, ~310 ch)", _SAMPLE_MEDIUM, 50_000),
        ("count_thai (long, ~6K ch)", _SAMPLE_LONG, 5_000),
        ("count_thai (huge, ~60K ch)", _SAMPLE_HUGE, 500),
    ]:
        rows_ct.append(bench(label, _py_count_thai, cy_count_thai, (text,), n))
    print_table("count_thai — Small-Scale vs Big-Scale", rows_ct)

    # ── Multi-Scale: remove_tonemark ───────────────────────────────────
    rows_rt = []
    for label, text, n in [
        ("remove_tonemark (short, ~25 ch)", _TONE_SHORT, 500_000),
        ("remove_tonemark (long, ~6K ch)", _TONE_LONG, 5_000),
    ]:
        rows_rt.append(
            bench(label, _py_remove_tonemark, cy_remove_tonemark, (text,), n)
        )
    print_table("remove_tonemark — Small-Scale vs Big-Scale", rows_rt)

    # ── cProfile Hotspot Analysis ──────────────────────────────────────
    print("=" * 72)
    print("cPROFILE HOTSPOT ANALYSIS")
    print("=" * 72)
    print(
        "  Profiling count_thai on long text (~6K chars) × 100K calls"
    )
    print("  to show where time is spent before/after Cython.\n")

    print("── BEFORE (Pure Python count_thai) ──")
    profile_out = profile_function(
        _py_count_thai,
        (_SAMPLE_LONG,),
        repeat=100_000,
    )
    print(profile_out)

    if cy_count_thai is not None:
        print("── AFTER (Cython count_thai) ──")
        profile_out = profile_function(
            cy_count_thai,
            (_SAMPLE_LONG,),
            repeat=100_000,
        )
        print(profile_out)

    print("── BEFORE (Pure Python remove_tonemark) ──")
    profile_out = profile_function(
        _py_remove_tonemark,
        (_TONE_LONG,),
        repeat=50_000,
    )
    print(profile_out)

    if cy_remove_tonemark is not None:
        print("── AFTER (Cython remove_tonemark) ──")
        profile_out = profile_function(
            cy_remove_tonemark,
            (_TONE_LONG,),
            repeat=50_000,
        )
        print(profile_out)

    print("=" * 72)
    print("BENCHMARK COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
