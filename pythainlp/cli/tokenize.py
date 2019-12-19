import argparse

from pythainlp import cli
from pythainlp.tokenize import word_tokenize, subword_tokenize, syllable_tokenize, sent_tokenize


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(
            **cli.make_usage("tokenize " + name)
        )
        parser.add_argument(
            "-t",
            "--text",
            type=str,
            help="input text",
        )

        parser.add_argument(
            "-s",
            "--sep",
            type=bool,
            help=f"default: {self.separator}",
            default=self.separator
        )

        parser.add_argument(
            "-e",
            "--engine",
            type=str,
            help=f"default: {self.engine}",
            default=self.engine
        )

        parser.add_argument(
            "-w",
            "--keep-whitespace",
            type=bool,
            help=f"default: {self.keep_whitespace}",
            default=self.keep_whitespace
        )

        args = parser.parse_args(argv)

        self.args = args

        cli.exit_if_empty(args.text, parser)

        result = self.run(args.text, engine=args.engine)
        print(self.separator.join(result))


class WordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.engine = "newmm"
        self.sep = "|"
        self.run = word_tokenize

        super().__init__(*args, **kwargs)


class SyllableTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.engine = "ssg"
        self.sep = "~"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class SentenceTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.engine = "crfcut"
        self.sep = "^"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class SubwordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.engine = "tcc"
        self.sep = "/"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tokenize"))
        parser.add_argument(
            "command",
            type=str,
            nargs="?",
            help="[subword|syllable|word|sent]"
        )

        args = parser.parse_args(argv[2:3])
        command = args.command

        cli.exit_if_empty(command, parser)

        argv = argv[3:]

        if command == "word":
            WordTokenizationApp("word", argv)
        elif command == "syllable":
            SyllableTokenizationApp("syllable", argv)
