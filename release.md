# How to cut a new release

0. Check if the package can be built properly.
   Add the prefix "[cd build]" to the commit message to trigger wheel building.
1. This project follows [semantic versioning][semver].
   Ensure the version and release date fields (if any) in these files
   have been updated to the version of the new planned release:
    - `pyproject.toml`
    - `setup.cfg`
    - `setup.py`
    - `CITATION.cff`
    - `README.md`
    - `README.TH.md`
    - `CHANGELOG.md`
2. Navigate to the [releases page][releases] and click the
   "Draft a new release" button.
   Only project maintainers are able to perform this step.
3. Then enter the new tag in the "Choose a tag" box.
   The tag should begin with "v", as in, for instance, `v5.0.1`.
4. The release title should be the same as the new version tag.
   For instance, the title could be `v5.0.1`.
5. Add a short summary of important changes in this release.
   For example, deprecation or termination of support.
6. Then click the "Generate release notes" button.
7. You can optionally include any particular thank-you's to contributors or
   reviewers in a note at the bottom of the release.
8. You can then click "Publish release" button.
9. If [the CI][ci] run is [successful][actions],
   then the release will be published on both
   the GitHub release page and also the [Python Package Index][pypi].

[semver]: https://semver.org/
[releases]: https://github.com/PyThaiNLP/pythainlp/releases
[ci]: https://github.com/PyThaiNLP/pythainlp/blob/dev/.github/workflows/pypi-publish.yml
[actions]: https://github.com/PyThaiNLP/pythainlp/actions/workflows/pypi-publish.yml
[pypi]: https://pypi.org/project/pythainlp/
