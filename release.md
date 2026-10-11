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

   On a branch from `main`, rename `[Unreleased]` to
   `[MAJOR.MINOR.PATCH] - YYYY-MM-DD`, with a new empty `[Unreleased]`
   above it. Update the "Commit history" link at the top and the link
   definitions at the bottom. Follow the [Keep a Changelog][keepachangelog]
   format.

3. **Update version using bump-my-version**

   We use [`bump-my-version`][bump-my-version] to manage version numbers.
   The configuration is in `pyproject.toml` under `[tool.bumpversion]`.

   Version format: `MAJOR.MINOR.PATCH[-RELEASE][BUILD]`
   where RELEASE can be `dev`, `beta`, or omitted (production).

   **To bump the version:**

   ```sh
   # Go straight to a production version (e.g., 5.3.8 -> 5.4.0)
   bump-my-version bump --new-version 5.4.0

   # Or step through the parts
   # (e.g., 5.2.0 -> 5.2.1-dev0, 5.3.0-dev0, or 6.0.0-dev0)
   bump-my-version bump patch   # or minor, or major

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
   - `README.md` and `README_TH.md` - version row and `dev` compare link

   The release dates are automatically set to the current date when you run
   the bump command.

   It also creates a git commit, but no tag (`tag = false`): the tag must
   point to the commit that lands on `main`, which a pull request can change
   (step 5).

   Bump to a production version on the release branch. A dev or beta version
   would also go into the README files.

4. **Update the other version references by hand**

   - `SECURITY.md`: the supported versions table

5. **Merge to main, then tag**

   Open a pull request from the branch to `main` (the default branch for
   releases), and wait for CI. After the merge:

   ```sh
   git fetch upstream
   git tag vX.Y.Z upstream/main    # check that this is the merged commit
   git push upstream vX.Y.Z
   ```

6. **Create GitHub Release**

   Navigate to the [releases page][releases] and click the
   "Draft a new release" button.
   Only project maintainers are able to perform this step.

7. **Select the tag**

   In the "Choose a tag" dropdown, select the tag that you pushed in step 5
   (e.g., `v5.2.1`). Tags follow the format `vMAJOR.MINOR.PATCH`.

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

13. **Create the maintenance branch**

    For a new minor or major version, create a branch named `MAJOR.MINOR`
    from the tag (e.g., `5.4` from `v5.4.0`) before `main` moves on.
    Later patch releases of that line (`5.4.x`) are cut from this branch.

14. **Sync main into dev**

    Merge `main` into `dev` with a merge commit, through a pull request
    from a branch that does not track `upstream`. Do this last, so `dev`
    gets the version bump, the change log, and the tag. Keep the `dev`
    version string if it differs.

[semver]: https://semver.org/
[keepachangelog]: https://keepachangelog.com/en/1.0.0/
[bump-my-version]: https://github.com/callowayproject/bump-my-version
[releases]: https://github.com/PyThaiNLP/pythainlp/releases
[ci]: https://github.com/PyThaiNLP/pythainlp/blob/dev/.github/workflows/pypi-publish.yml
[actions]: https://github.com/PyThaiNLP/pythainlp/actions/workflows/pypi-publish.yml
[pypi]: https://pypi.org/project/pythainlp/
