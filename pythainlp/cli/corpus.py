import argparse

from pythainlp import corpus

class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser("corpus")
        parser.add_argument("subcommand",
            type=str,
            help="[download|remove]"
        )

        parser.add_argument("--name",
            type=str,
            help="corpus's name",
        )

        args = parser.parse_args(argv[2:])
        subcommand = args.subcommand

        if hasattr(App, subcommand):
            getattr(App, subcommand)(args)
        else:
            print("No subcommand available: %s" % subcommand)

    @staticmethod
    def download(args):
        corpus.download(args.name)

    @staticmethod
    def remove(args):
        corpus.remove(args.name)
