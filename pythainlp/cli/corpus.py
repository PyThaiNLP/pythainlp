import argparse

from pythainlp import corpus, cli


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("corpus"))

        parser.add_argument(
            "subcommand",
            type=str,
            default="",
            nargs="?",
            help="[download|remove]"  # there should be a "list" subcommand
        )

        parser.add_argument(
            "--name",
            type=str,
            help="corpus's name",
        )

        args = parser.parse_args(argv[2:])

        cli.exit_if_empty(args.subcommand, parser)
        subcommand = str.lower(args.subcommand)

        if hasattr(App, subcommand):
            getattr(App, subcommand)(args)
        else:
            raise NotImplementedError(f"Subcommand not available: {subcommand}")

    @staticmethod
    def download(args):
        corpus.download(args.name)

    @staticmethod
    def remove(args):
        corpus.remove(args.name)
