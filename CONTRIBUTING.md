# Contributing to PyThaiNLP

Hi! Thanks for your interest in contributing to [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp).

Please refer to our [Contributor Covenant Code of Conduct](https://github.com/PyThaiNLP/pythainlp/blob/dev/CODE_OF_CONDUCT.md).

## Issue Report and Discussion

- Discussion: https://github.com/PyThaiNLP/pythainlp/discussions
- GitHub issues (for problems and suggestions): https://github.com/PyThaiNLP/pythainlp/issues
- Facebook group (not specific to PyThaiNLP, for Thai NLP discussion in general): https://www.facebook.com/groups/thainlp


## Code

## Code Guidelines

- Follow [PEP8](http://www.python.org/dev/peps/pep-0008/), use [black](https://github.com/ambv/black) with `--line-length` = 79;
- Name identifiers (variables, classes, functions, module names) with meaningful
  and pronounceable names (`x` is always wrong);
  - Please follow this [naming convention](https://namingconvention.org/python/). For example, global constant variables must be in `ALL_CAPS`;
  <img src="https://i.stack.imgur.com/uBr10.png" />
- Write tests for your new features. The test suite is in `tests/` directory. (see "Testing" section below);
- Run all tests before pushing (just execute `tox`) so you will know if your
  changes broke something;
- Commented out codes are [dead
  codes](http://www.codinghorror.com/blog/2008/07/coding-without-comments.html);
- All `#TODO` comments should be turned into [issues](https://github.com/pythainlp/pythainlp/issues) in GitHub;
- When appropriate, use [f-string](https://www.python.org/dev/peps/pep-0498/)
  (use `f"{a} = {b}"`, instead of `"{} = {}".format(a, b)` and `"%s = %s' % (a, b)"`);
- All text files, including source codes, must end with one empty line. This is [to please git](https://stackoverflow.com/questions/5813311/no-newline-at-end-of-file#5813359) and [to keep up with POSIX standard](https://stackoverflow.com/questions/729692/why-should-text-files-end-with-a-newline).

### Version Control System

- We use [Git](http://git-scm.com/) as our [version control system](http://en.wikipedia.org/wiki/Revision_control),
so it may be a good idea to familiarize yourself with it.
- You can start with the [Pro Git book](http://git-scm.com/book/) (free!).

### Commit Message

- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Commit Verbs 101: why I like to use this and why you should also like it.](https://chris.beams.io/posts/git-commit/)

### Pull Request

- We use the famous [gitflow](http://nvie.com/posts/a-successful-git-branching-model/)
to manage our branches.
- When you create pull requests on GitHub, Github Actions and AppVeyor will run tests
and several checks automatically. Click the "Details" link at the end of
each check to see what needs to be fixed.


## Documentation

- We use [Sphinx](https://www.sphinx-doc.org/en/master/) to generate API document
automatically from "docstring" comments in source codes. This means the comment
section in the source codes is important for the quality of documentation.
- A docstring should start with one summary line, end with one line with a full stop (period),
then be followed by a blank line before starting a new paragraph.
- A commit to release branches (e.g. `2.2`, `2.1`) with a title **"(build and deploy docs)"** (without quotes) will trigger the system to rebuild the documentation files and upload them to the website https://pythainlp.github.io/docs.


## Testing

We use standard Python `unittest`. The test suite is in `tests/` directory.

To run unit tests locally together with code coverage test:

(from main `pythainlp/` directory)
```sh
coverage run -m unittest discover
```

See code coverage test:
```sh
coverage report
```

Generate code coverage test in HTML (files will be available in `htmlcov/` directory):
```sh
coverage html
```

Make sure the tests pass on both Github Actions and AppVeyor.


## Releasing
- We use [semantic versioning](https://semver.org/): MAJOR.MINOR.PATCH, with development build suffix: MAJOR.MINOR.PATCH-devBUILD
- We use [`bumpversion`](https://github.com/c4urself/bump2version/#installation) to manage versioning.
  - `bumpversion [major|minor|patch|release|build]`
  - Example:
  ```
  #current_version = 2.3.3-dev0

  bumpversion build
  #current_version = 2.3.3-dev1

  bumpversion build
  #current_version = 2.3.3-dev2

  bumpversion release
  #current_version = 2.3.3-beta0
  
  bumpversion release
  #current_version = 2.3.3

  bumpversion patch
  #current_version = 2.3.6-dev0

  bumpversion minor
  #current_version = 2.3.1-dev0

  bumpversion build
  #current_version = 2.3.1-dev1

  bumpversion major
  #current_version = 3.0.0-dev0

  bumpversion release
  #current_version = 3.0.0-beta0

  bumpversion release
  #current_version = 3.0.0
  ```

## Credits

<a href="https://github.com/PyThaiNLP/pythainlp/graphs/contributors">
  <img src="https://contributors-img.firebaseapp.com/image?repo=PyThaiNLP/pythainlp" />
</a>

Thanks to all [contributors](https://github.com/PyThaiNLP/pythainlp/graphs/contributors). (Image made with [contributors-img](https://contributors-img.firebaseapp.com))

### Development Leads
- Wannaphong Phatthiyaphaibun <wannaphong@yahoo.com> - foundation, distribution and maintenance
- Korakot Chaovavanich - initial tokenization and soundex codes
- Charin Polpanumas - classification and benchmarking
- Arthit Suriyawongkul - refactoring, packaging, distribution, and maintenance
- Lalita Lowphansirikul - documentation
- Pattarawat Chormai - benchmarking
- Peerat Limkonchotiwat
- Thanathip Suntorntip - nlpO3 maintenance, Rust Developer
- Can Udomcharoenchaikit - documentation and codes

### Maintainers
- Arthit Suriyawongkul
- Wannaphong Phatthiyaphaibun


### Past
- Peeradej Tanruangporn - documentation

## References

- **[Maximum Matching]** -- Manabu Sassano. Deterministic Word Segmentation Using Maximum Matching with Fully Lexicalized Rules. Retrieved from http://www.aclweb.org/anthology/E14-4016
- **[MetaSound]** -- Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with a Statistical Ontology for Analysing Names Given in Accordance with Thai Astrology. Retrieved from https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf
- **[Thai Character Cluster]** -- T. Teeramunkong, V. Sornlertlamvanich, T. Tanhermhong and W. Chinnan, “Character cluster based Thai information retrieval,” in IRAL '00 Proceedings of the fifth international workshop on on Information retrieval with Asian languages, 2000.
- **[Enhanced Thai Character Cluster]** -- Jeeragone Inrut, Patiroop Yuanghirun, Sarayut Paludkong, Supot Nitsuwat, and Para Limmaneepraserth. “Thai word segmentation using combination of forward and backward longest matching techniques.” In International Symposium on Communications and Information Technology (ISCIT), pp. 37-40. 2001.
- เพ็ญศิริ ลี้ตระกูล. การเลือกประโยคสำคัญในการสรุปความภาษาไทย โดยใช้แบบจำลองแบบลำดับชั้น (Selection of Important Sentences in Thai Text Summarization Using a Hierarchical Model). Retrieved from http://digi.library.tu.ac.th/thesis/st/0192/
