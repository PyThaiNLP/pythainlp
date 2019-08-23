import argparse

from pythainlp import corpus, cli


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("corpus"))

        parser.add_argument(
            "--name",
            type=str,
            help="corpus's name",
        )

        parser.add_argument(
            "command",
            type=str,
            default="",
            nargs="?",
            help="[download|remove]"
        )

        args = parser.parse_args(argv[2:])

        cli.exit_if_empty(args.command, parser)
        command = args.command

        if hasattr(App, command):
            getattr(App, command)(args)
        else:
            print("No command available: %s" % command)

    @staticmethod
    def download(args):
        corpus.download(args.name)

    @staticmethod
    def remove(args):
        corpus.remove(args.name)
