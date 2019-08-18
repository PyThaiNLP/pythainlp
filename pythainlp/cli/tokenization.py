import argparse

from pythainlp.tokenize import word_tokenize, syllable_tokenize


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(name)
        parser.add_argument("--text",
                            type=str,
                            help="input text",
                            )

        parser.add_argument("--engine",
                            type=str,
                            help="text",  # TODO: add all available engines
                            default=self.default_engine
                            )

        args = parser.parse_args(argv)

        print(f"Using engine={args.engine}")

        self.args = args

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
        parser = argparse.ArgumentParser("corpus")
        parser.add_argument("subcommand",
                            type=str,
                            help="[word|syllable]"
                            )

        args = parser.parse_args(argv[2:3])
        subcommand = args.subcommand

        argv = argv[3:]

        if subcommand == "word":
            WordTokenizationApp("word tokenization", argv)
        elif subcommand == "syllable":
            SyllableTokenizationApp("syllable tokenization", argv)
