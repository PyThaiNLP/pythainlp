# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Update documentation index pages on release.

This script performs two tasks:

1. Generates or updates ``index.html`` in the versioned docs repository
   (``PyThaiNLP/docs``) to list all released versions as a landing page.
2. Injects or updates a released-versions section in ``index.html`` of the
   development docs repository (``PyThaiNLP/dev-docs``).

Usage::

    python update_docs_index.py \\
        --docs-dir /path/to/docs \\
        --dev-docs-index /path/to/dev-docs/index.html \\
        --version 5.3.1
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Markers used to delimit the injected versions section in dev-docs/index.html.
_VERSIONS_BEGIN: str = "<!-- BEGIN VERSIONS -->"
_VERSIONS_END: str = "<!-- END VERSIONS -->"

_VERSIONS_SECTION_TMPL: str = """\
<!-- BEGIN VERSIONS -->
<section id="released-versions">
  <h2>Released versions</h2>
  <ul>
{items}
  </ul>
</section>
<!-- END VERSIONS -->"""

_VERSION_ITEM_TMPL: str = (
    '    <li><a href="https://pythainlp.github.io/docs/{v}/">{v}</a></li>'
)

_DOCS_INDEX_TMPL: str = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PyThaiNLP Documentation</title>
  <style>
    body {{
      font-family: sans-serif;
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1rem;
    }}
    h1 {{ color: #333; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 0.5rem 0; }}
    a {{ color: #0066cc; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <h1>PyThaiNLP Documentation</h1>
  <p>
    Latest development docs:
    <a href="https://pythainlp.github.io/dev-docs/">dev-docs</a>
  </p>
  <h2>Released versions</h2>
  <ul>
{items}
  </ul>
</body>
</html>
"""


def _is_version_dir(name: str) -> bool:
    """Return True if *name* looks like a version directory (e.g. ``5.3.1``)."""
    return bool(re.match(r"^\d+\.\d+", name))


def _version_key(version: str) -> tuple:
    """Return a sort key for a version string."""
    parts = re.split(r"[.\-]", version)
    key: list[int] = []
    for part in parts:
        try:
            key.append(int(part))
        except ValueError:
            break
    return tuple(key)


def _get_version_dirs(docs_dir: Path) -> list[str]:
    """Return version directories in *docs_dir*, sorted newest-first."""
    versions = [
        p.name
        for p in docs_dir.iterdir()
        if p.is_dir() and _is_version_dir(p.name)
    ]
    versions.sort(key=_version_key, reverse=True)
    return versions


def update_docs_index(docs_dir: Path) -> None:
    """Generate or overwrite ``docs_dir/index.html`` listing all versions.

    :param docs_dir: Path to the versioned documentation repository root.
    """
    versions = _get_version_dirs(docs_dir)
    items = "\n".join(
        f'    <li><a href="{v}/">{v}</a></li>' for v in versions
    )
    content = _DOCS_INDEX_TMPL.format(items=items)
    index_path = docs_dir / "index.html"
    index_path.write_text(content, encoding="utf-8")
    print(f"Updated {index_path}")


def update_dev_docs_index(index_path: Path, version: str) -> None:
    """Inject or update a released-versions section in *index_path*.

    Looks for ``<!-- BEGIN VERSIONS -->`` / ``<!-- END VERSIONS -->`` markers.
    If found, prepends *version* to the existing list (skips if already there).
    If not found, appends a new section before ``</body>`` (or at end of file).

    :param index_path: Path to ``dev-docs/index.html``.
    :param version: Version string without leading ``v`` (e.g. ``5.3.1``).
    """
    content = index_path.read_text(encoding="utf-8")
    new_item = _VERSION_ITEM_TMPL.format(v=version)

    if _VERSIONS_BEGIN in content and _VERSIONS_END in content:
        begin = content.index(_VERSIONS_BEGIN)
        end = content.index(_VERSIONS_END) + len(_VERSIONS_END)
        section = content[begin:end]

        # Skip if this version is already listed.
        if f"/{version}/" in section:
            print(f"{index_path}: version {version} already present, skipping.")
            return

        # Prepend the new item inside the existing <ul> or <ol>.
        section = re.sub(
            r"(<[uo]l[^>]*>)",
            rf"\1\n{new_item}",
            section,
            count=1,
        )
        content = content[:begin] + section + content[end:]
    else:
        # No markers yet — append a new section.
        new_section = _VERSIONS_SECTION_TMPL.format(items=new_item)
        if "</body>" in content:
            content = content.replace("</body>", f"\n{new_section}\n</body>")
        else:
            content = content + f"\n{new_section}\n"

    index_path.write_text(content, encoding="utf-8")
    print(f"Updated {index_path}")


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Update PyThaiNLP documentation index pages on release.",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        help=(
            "Path to the versioned docs repository. "
            "Generates or overwrites index.html listing all version directories."
        ),
    )
    parser.add_argument(
        "--dev-docs-index",
        type=Path,
        help=(
            "Path to dev-docs/index.html. "
            "Injects or updates a released-versions section."
        ),
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Version string without leading 'v' (e.g. 5.3.1).",
    )
    args = parser.parse_args()

    if not args.docs_dir and not args.dev_docs_index:
        parser.error("At least one of --docs-dir or --dev-docs-index is required.")

    if args.docs_dir:
        if not args.docs_dir.is_dir():
            print(
                f"Error: --docs-dir '{args.docs_dir}' is not a directory.",
                file=sys.stderr,
            )
            sys.exit(1)
        update_docs_index(args.docs_dir)

    if args.dev_docs_index:
        if not args.dev_docs_index.exists():
            print(
                f"Warning: --dev-docs-index '{args.dev_docs_index}' does not exist, "
                "skipping.",
                file=sys.stderr,
            )
        else:
            update_dev_docs_index(args.dev_docs_index, args.version)


if __name__ == "__main__":
    main()
