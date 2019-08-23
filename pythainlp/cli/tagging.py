import argparse

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
            help="text", 
            default=self.default_engine
        )

        parser.add_argument(
            "--corpus",
            type=str,
            help="text", 
            default=self.default_corpus
        )

        parser.add_argument(
            '--sep',
            type=str,
            help="separator",
            default="|"
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
        self.run = pos_tag

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser("tagging")
        parser.add_argument(
            "subcommand",
            type=str,
            help="[pos]"
        )

        ['ฉัน','มี','ชีวิต','รอด','ใน','อาคาร','หลบภัย','ของ', 'นายก', 'เชอร์ชิล']

        args = parser.parse_args(argv[2:3])
        subcommand = args.subcommand

        argv = argv[3:]

        if subcommand == "pos":
            POSTaggingApp("Part-of-Speech tagging", argv)
        else:
            raise ValueError(f"no command:{subcommand}")
