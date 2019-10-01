# Contributing to PyThaiNLP

Hi! Thanks for your interest in contributing to [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp).
In this document we'll try to summarize everything that you need to know to
do a good job.

## Contributing to Code and Documentation

### Git

We use [Git](http://git-scm.com/) as our [version control system](http://en.wikipedia.org/wiki/Revision_control),
so the best way to contribute is to learn how to use it and put your changes on a Git repository.
There's a plenty of documentation about Git -- you can start with the [Pro Git
book](http://git-scm.com/book/).

### Forks + GitHub Pull Requests

We use the famous [gitflow](http://nvie.com/posts/a-successful-git-branching-model/) to manage our branches.

## Code Guidelines

- Follows [PEP8](http://www.python.org/dev/peps/pep-0008/), use [black](https://github.com/ambv/black);
- Write tests for your new features (please see "Tests" topic below);
- Always remember that [commented code is dead
  code](http://www.codinghorror.com/blog/2008/07/coding-without-comments.html);
- Name identifiers (variables, classes, functions, module names) with meaningful
  and pronounceable names (`x` is always wrong);
- When appropriate, use [f-String](https://www.python.org/dev/peps/pep-0498/)
  (use `f"{a} = {b}"`, instead of `"{} = {}".format(a, b)` and `"%s = %s' % (a, b)"`);
- All `#TODO` comments should be turned into issues (use our
  [GitHub issue system](https://github.com/PyThaiNLP/pythainlp/));
- Run all tests before pushing (just execute `tox`) so you will know if your
  changes broke something;
- All source code and all text files should be ended with one empty line. This is [to please git](https://stackoverflow.com/questions/5813311/no-newline-at-end-of-file#5813359) and also [to keep up with POSIX standard](https://stackoverflow.com/questions/729692/why-should-text-files-end-with-a-newline).


# Discussion

- GitHub issues (PyThaiNLP problems and suggestions): https://github.com/PyThaiNLP/pythainlp/issues
- Facebook group (Thai NLP discussion in general, not specific to PyThaiNLP): https://www.facebook.com/groups/thainlp 

Happy hacking! (;


# Credits

## Development Lead
- Wannaphong Phatthiyaphaibun <wannaphong@kkumail.com>
- Korakot Chaovavanich
- Charin Polpanumas
- Peeradej Tanruangporn
- Arthit Suriyawongkul
- Chakri Lowphansirikul
- Pattarawat Chormai

## newmm (onecut), mm, TCC, and Thai Soundex Code
- Korakot Chaovavanich

## thai2fit & ULMFiT
- Charin Polpanumas

## Docs
- Peeradej Tanruangporn
- Chakri Lowphansirikul

## Maintainers
- Arthit Suriyawongkul
- Wannaphong Phatthiyaphaibun

## Benchmark
- Charin Polpanumas
- Pattarawat Chormai

## Contributors
- See more contributions here https://github.com/PyThaiNLP/pythainlp/graphs/contributors


# References

- **[Maximum Matching]** -- Manabu Sassano. Deterministic Word Segmentation Using Maximum Matching with Fully Lexicalized Rules. Retrieved from http://www.aclweb.org/anthology/E14-4016
- **[MetaSound]** -- Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with a Statistical Ontology for Analysing Names Given in Accordance with Thai Astrology. Retrieved from https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf
- **[Thai Character Cluster]** -- T. Teeramunkong, V. Sornlertlamvanich, T. Tanhermhong and W. Chinnan, “Character cluster based Thai information retrieval,” in IRAL '00 Proceedings of the fifth international workshop on on Information retrieval with Asian languages, 2000. 
- เพ็ญศิริ ลี้ตระกูล. การเลือกประโยคสำคัญในการสรุปความภาษาไทย โดยใช้แบบจำลองแบบลำดับชั้น (Selection of Important Sentences in Thai Text Summarization Using a Hierarchical Model). Retrieved from http://digi.library.tu.ac.th/thesis/st/0192/
