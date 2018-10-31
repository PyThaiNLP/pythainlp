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

- Use [PEP8](http://www.python.org/dev/peps/pep-0008/);
- Write tests for your new features (please see "Tests" topic below);
- Always remember that [commented code is dead
  code](http://www.codinghorror.com/blog/2008/07/coding-without-comments.html);
- Name identifiers (variables, classes, functions, module names) with readable
  names (`x` is always wrong);
- When manipulating strings, use [Python's new-style
  formatting](http://docs.python.org/library/string.html#format-string-syntax)
  (`'{} = {}'.format(a, b)` instead of `'%s = %s' % (a, b)`);
- All `#TODO` comments should be turned into issues (use our
  [GitHub issue system](tps://github.com/wannaphongcom/pythainlp/));
- Run all tests before pushing (just execute `tox`) so you will know if your
  changes broke something;


# Discussion

- Facebook group: https://www.facebook.com/groups/thainlp 
- GitHub issues: https://github.com/wannaphongcom/pythainlp/issues

Happy hacking! (;


# Credits

## Development Lead
- Wannaphong Phatthiyaphaibun <wannaphong@kkumail.com>
- Korakot Chaovavanich
- Charin Polpanumas
- Peeradej Tanruangporn
- Arthit Suriyawongkul

## newmm (onecut), mm, TCC, and Thai Soundex Code
- Korakot Chaovavanich

## Thai2Vec & ulmfit
- Charin Polpanumas

## Docs
- Peeradej Tanruangporn

## Contributors
- See more contributions here https://github.com/wannaphongcom/pythainlp/graphs/contributors


# References

- **[Maximum Matching]** -- Manabu Sassano. Deterministic Word Segmentation Using Maximum Matching with Fully Lexicalized Rules. Retrieved from http://www.aclweb.org/anthology/E14-4016
- **[MetaSound]** -- Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with a Statistical Ontology for Analysing Names Given in Accordance with Thai Astrology. Retrieved from https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf
- **[Thai Character Cluster]** -- T. Teeramunkong, V. Sornlertlamvanich, T. Tanhermhong and W. Chinnan, “Character cluster based Thai information retrieval,” in IRAL '00 Proceedings of the fifth international workshop on on Information retrieval with Asian languages, 2000. 
- เพ็ญศิริ ลี้ตระกูล. การเลือกประโยคสำคัญในการสรุปความภาษาไทย โดยใช้แบบจำลองแบบลำดับชั้น (Selection of Important Sentences in Thai Text Summarization Using a Hierarchical Model). Retrieved from http://digi.library.tu.ac.th/thesis/st/0192/
