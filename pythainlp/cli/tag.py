"""
thainlp tag command line.
"""
import argparse

from pythainlp import cli
from pythainlp.tag import locations, named_entity, pos_tag


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(name)
        parser.add_argument(
            "text", type=str, help="input text",
        )

        parser.add_argument(
            "-s",
            "--sep",
            dest="separator",
            type=str,
            help=f"Token separator for input text. default: {self.separator}",
            default=self.separator,
        )

        args = parser.parse_args(argv)
        self.args = args

        tokens = args.text.split(args.separator)
        result = self.run(tokens)

        for word, tag in result:
            print(word, "/", tag)


class POSTaggingApp(SubAppBase):
    def __init__(self, *args, **kwargs):
        self.separator = "|"
        self.run = pos_tag

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tag"))
        parser.add_argument("subcommand", type=str, help="[pos]")

        args = parser.parse_args(argv[2:3])

        cli.exit_if_empty(args.subcommand, parser)
        subcommand = str.lower(args.subcommand)

        argv = argv[3:]

        if subcommand == "pos":
            POSTaggingApp("Part-of-Speech tagging", argv)
        else:
            print(f"Tag type not available: {subcommand}")
