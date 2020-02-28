import argparse

from pythainlp import cli
from pythainlp.tag import pos_tag


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(name)
        parser.add_argument(
            "--text",
            type=str,
            help="input text",
        )

        parser.add_argument(
            "--engine",
            type=str,
            help=f"default: {self.engine}",
            default=self.engine
        )

        parser.add_argument(
            "--corpus",
            type=str,
            help=f"default: {self.corpus}",
            default=self.corpus
        )

        parser.add_argument(
            "-s",
            "--sep",
            type=str,
            help=f"default: {self.sep}",
            default=self.sep
        )

        args = parser.parse_args(argv)
        self.args = args

        result = self.run(
            args.text.split(args.sep), engine=args.engine, corpus=args.corpus
        )

        result_str = map(lambda x: f"{x}/{result}")

        print(" ".join(result_str))


class POSTaggingApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.engine = "perceptron"
        self.corpus = "orchid"
        self.sep = "|"
        self.run = pos_tag

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tag"))
        parser.add_argument(
            "subcommand",
            type=str,
            nargs="?",
            help="[pos]"
        )

        args = parser.parse_args(argv[2:3])

        cli.exit_if_empty(args.subcommand, parser)
        subcommand= str.lower(args.subcommand)

        argv = argv[3:]

        if subcommand == "pos":
            POSTaggingApp("Part-of-Speech tagging", argv)
        else:
            raise NotImplementedError(f"Subcommand not available: {subcommand}")
