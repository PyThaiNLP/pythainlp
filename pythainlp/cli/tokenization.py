import argparse

from pythainlp.tokenize import word_tokenize, syllable_tokenize

class App:

    default_engine = {
        "word": "newmm",
        "syllable": "ssg"
    }

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

        parser.add_argument("--engine",
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
    def word(args, default_engine="newmm"):
        engine = App._get_engine(args)

        tokens = word_tokenize(args.text, engine=engine)
        print("|".join(tokens))

    @staticmethod
    def syllable(args, default_engine="ssg"):
        engine = App._get_engine(args)

        syllables = syllable_tokenize(args.text)
        print("|".join(syllables))

    @staticmethod
    def _get_engine(args):
        engine = args.engine if args.engine else App.default_engine[args.subcommand]
        print(f"Using engine={engine}")

        return engine
