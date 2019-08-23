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
            help="default: %s" % self.default_engine,
            default=self.default_engine
        )

        parser.add_argument(
            "--corpus",
            type=str,
            help="default: %s" % self.default_corpus,
        )

        parser.add_argument(
            '--sep',
            type=str,
            help="default: %s" % self.default_sep,
            default=self.default_sep
        )

        args = parser.parse_args(argv)

        print(f"Using engine={args.engine}")

        self.args = args

        result = self.run(
            args.text.split(args.sep), engine=args.engine, corpus=args.corpus
        )

        result_str = map(lambda x: "%s/%s" % x, result)

        print(" ".join(result_str))


class POSTaggingApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.default_engine = "perceptron"
        self.default_corpus = "orchid"
        self.default_sep = "|"
        self.run = pos_tag

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tagging"))
        parser.add_argument(
            "command",
            type=str,
            nargs="?",
            help="[pos]"
        )

        args = parser.parse_args(argv[2:3])
        command = args.command

        cli.exit_if_empty(args.command, parser)

        argv = argv[3:]

        if command == "pos":
            POSTaggingApp("Part-of-Speech tagging", argv)
        else:
            raise ValueError(f"no command:{subcommand}")
