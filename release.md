---
SPDX-FileCopyrightText: 2025-2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# How to cut a new release

This project follows [semantic versioning][semver].

## Prerequisites

Install development dependencies including `bump-my-version`:

```sh
pip install -e ".[dev]"
```

## Release Process

1. **Check if the package can be built properly**

   Build the package locally to ensure there are no build errors:

   ```sh
   python -m build
   ```

   You can also include `[cd build]` in a commit message to trigger wheel
   building in CI.

2. **Update CHANGELOG.md**

   Update `CHANGELOG.md` with a short summary of important changes since
   the previous stable release. For example, deprecation or termination
   of support. Follow the [Keep a Changelog][keepachangelog] format.

3. **Update version using bump-my-version**

   We use [`bump-my-version`][bump-my-version] to manage version numbers.
   The configuration is in `pyproject.toml` under `[tool.bumpversion]`.

   Version format: `MAJOR.MINOR.PATCH[-RELEASE][BUILD]`
   where RELEASE can be `dev`, `beta`, or omitted (production).

   **To bump the version:**

   ```sh
   # For a patch release (e.g., 5.2.0 -> 5.2.1-dev0)
   bump-my-version bump patch

   # For a minor release (e.g., 5.2.0 -> 5.3.0-dev0)
   bump-my-version bump minor

   # For a major release (e.g., 5.2.0 -> 6.0.0-dev0)
   bump-my-version bump major

   # To move from dev to beta (e.g., 5.2.1-dev0 -> 5.2.1-beta0)
   bump-my-version bump release

   # To move from beta to production (e.g., 5.2.1-beta0 -> 5.2.1)
   bump-my-version bump release

   # To increment build number (e.g., 5.2.1-dev0 -> 5.2.1-dev1)
   bump-my-version bump build
   ```

   This command will automatically update version numbers and release dates in:
   - `pyproject.toml` - version number
   - `pythainlp/__init__.py` - version number
   - `CITATION.cff` - version number and `date-released` field
   - `codemeta.json` - version number and `dateModified` field

   The release dates are automatically set to the current date when you run
   the bump command.

   It will also create a git commit and tag by default.

4. **Update README files if needed**

   If the release introduces significant changes, update:
   - `README.md`
   - `README_TH.md`

5. **Push changes and tag**

   ```sh
   git push origin dev
   git push origin --tags
   ```

6. **Create GitHub Release**

   Navigate to the [releases page][releases] and click the
   "Draft a new release" button.
   Only project maintainers are able to perform this step.

7. **Select the tag**

   In the "Choose a tag" dropdown, select the tag that was created by
   `bump-my-version` (e.g., `v5.2.1`). Tags follow the format `vMAJOR.MINOR.PATCH`.

8. **Set release title**

   The release title should be the same as the version tag
   (e.g., `v5.2.1`).

9. **Add release notes**

    Add a short summary of important changes since the previous stable
    release. This should be similar to what has been logged in `CHANGELOG.md`.
    Then click the "Generate release notes" button to auto-generate
    contributor information.

10. **Optional: Thank contributors**

    You can optionally include any particular thank-yous to contributors or
    reviewers in a note at the bottom of the release.

11. **Publish the release**

    Click the "Publish release" button.

12. **Verify CI/CD**

    If [the CI][ci] run is [successful][actions],
    then the release will be published on both
    the GitHub release page and the [Python Package Index][pypi].

[semver]: https://semver.org/
[keepachangelog]: https://keepachangelog.com/en/1.0.0/
[bump-my-version]: https://github.com/callowayproject/bump-my-version
[releases]: https://github.com/PyThaiNLP/pythainlp/releases
[ci]: https://github.com/PyThaiNLP/pythainlp/blob/dev/.github/workflows/pypi-publish.yml
[actions]: https://github.com/PyThaiNLP/pythainlp/actions/workflows/pypi-publish.yml
[pypi]: https://pypi.org/project/pythainlp/
