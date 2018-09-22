# Contributing to PyThaiNLP

Hi! Thanks for your interest in contributing to [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp).
In this document we'll try to summarize everything that you need to know to
do a good job.

## Git

### Git

We use [Git](http://git-scm.com/) as our [version control
system](http://en.wikipedia.org/wiki/Revision_control), so the best way to
contribute is to learn how to use it and put your changes on a Git repository.
There's a plenty of documentation about Git -- you can start with the [Pro Git
book](http://git-scm.com/book/).

### Forks + GitHub Pull requests

We use the famous
[gitflow](http://nvie.com/posts/a-successful-git-branching-model/) to manage our
branches.

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
- Try to write both Python 2 and Python3-friendly code so won't be a pain for
  us to support both versions.

# Discussion

https://www.facebook.com/groups/thainlp and https://github.com/wannaphongcom/pythainlp/issues

Happy hacking! (;
