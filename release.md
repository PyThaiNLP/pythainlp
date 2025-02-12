---
SPDX-FileCopyrightText: 2025 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# How to cut a new release

0. Check if the package can be built properly.
   Include "[cd build]" in the commit message to trigger wheel building.
1. Update `CHANGELOG.md` with a short summary of important changes since
   the previous stable release.
   For example, deprecation or termination of support.
3. This project follows [semantic versioning][semver].
   Ensure the version and release date fields (if any) in these files
   have been updated to the version of the new planned release:
    - `codemeta.json`
    - `pyproject.toml`
    - `setup.cfg`
    - `setup.py`
    - `CHANGELOG.md`
    - `CITATION.cff`
    - `README.md`
    - `README.TH.md`
4. Navigate to the [releases page][releases] and click the
   "Draft a new release" button.
   Only project maintainers are able to perform this step.
5. Then enter the new tag in the "Choose a tag" box.
   The tag should begin with "v", as in, for instance, `v5.0.1`.
6. The release title should be the same as the new version tag.
   For instance, the title could be `v5.0.1`.
7. Add a short summary of important changes since the previous stable
   release.
   _This should be similar to what have been logged in `CHANGELOG.md`._
   Then click the "Generate release notes" button.
9. You can optionally include any particular thank-you's to contributors or
   reviewers in a note at the bottom of the release.
10. You can then click "Publish release" button.
11. If [the CI][ci] run is [successful][actions],
   then the release will be published on both
   the GitHub release page and also the [Python Package Index][pypi].

[semver]: https://semver.org/
[releases]: https://github.com/PyThaiNLP/pythainlp/releases
[ci]: https://github.com/PyThaiNLP/pythainlp/blob/dev/.github/workflows/pypi-publish.yml
[actions]: https://github.com/PyThaiNLP/pythainlp/actions/workflows/pypi-publish.yml
[pypi]: https://pypi.org/project/pythainlp/
