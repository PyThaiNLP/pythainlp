import argparse

from pythainlp.tokenize import word_tokenize

class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser("corpus")
        parser.add_argument("subcommand",
            type=str,
            help="[word|syllable]"
        )

        parser.add_argument("--text",
            type=str,
            help="text",
        )

        args = parser.parse_args(argv[2:])
        subcommand = args.subcommand

        if hasattr(App, subcommand):
            getattr(App, subcommand)(args)
        else:
            print("No subcommand available: %s" % subcommand)

    @staticmethod
    def word(args):
        tokens = word_tokenize(args.text)
        print("|".join(tokens))

    @staticmethod
    def syllable(args):
        print("kenize syllable")
