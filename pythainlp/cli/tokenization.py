import argparse

from pythainlp import cli
from pythainlp.tokenize import word_tokenize, syllable_tokenize


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(
            **cli.make_usage("tokenization " + name)
        )
        parser.add_argument(
            "--text",
            type=str,
            help="input text",
        )

        parser.add_argument(
            "--engine",
            type=str,
            help="default: %s" % self.default_engine,
            default=self.default_engine
        )

        args = parser.parse_args(argv)

        self.args = args

        cli.exit_if_empty(args.text, parser)

        print(f"Using engine={args.engine}")
        result = self.run(args.text, engine=args.engine)
        print(self.separator.join(result))


class WordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.default_engine = "newmm"
        self.separator = "|"
        self.run = word_tokenize

        super().__init__(*args, **kwargs)


class SyllableTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.default_engine = "ssg"
        self.separator = "~"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tokenization"))
        parser.add_argument(
            "command",
            type=str,
            nargs="?",
            help="[word|syllable]"
        )

        args = parser.parse_args(argv[2:3])
        command = args.command

        cli.exit_if_empty(command, parser)

        argv = argv[3:]

        if command == "word":
            WordTokenizationApp("word", argv)
        elif command == "syllable":
            SyllableTokenizationApp("syllable", argv)
