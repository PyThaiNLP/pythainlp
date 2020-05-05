"""
thainlp dataset/corpus management command line.
"""
import argparse

from pythainlp import cli, corpus
from pythainlp.tools import get_pythainlp_data_path


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            prog="data", usage="thainlp data <subcommand>",
        )
        parser.add_argument(
            "subcommand",
            type=str,
            choices=["catalog", "info", "get", "rm", "path"],
            help="action on dataset/corpus",
        )
        args = parser.parse_args(argv[2:3])
        getattr(self, args.subcommand)(argv)

    def get(self, argv):
        parser = argparse.ArgumentParser(
            description="Download a dataset",
            usage="thainlp data get <dataset_name>",
        )
        parser.add_argument(
            "dataset_name", type=str, help="dataset/corpus's name",
        )
        args = parser.parse_args(argv[3:])
        if corpus.download(args.dataset_name):
            print("Downloaded successfully.")
        else:
            print("Not found.")

    def rm(self, argv):
        parser = argparse.ArgumentParser(
            description="Remove a dataset",
            usage="thainlp data rm <dataset_name>",
        )
        parser.add_argument(
            "dataset_name", type=str, help="dataset/corpus's name",
        )
        args = parser.parse_args(argv[3:])
        if corpus.remove(args.dataset_name):
            print("Removed successfully.")
        else:
            print("Not found.")

    def info(self, argv):
        parser = argparse.ArgumentParser(
            description="Print information about a dataset",
            usage="thainlp data info <dataset_name>",
        )
        parser.add_argument(
            "dataset_name", type=str, help="dataset/corpus's name",
        )
        args = parser.parse_args(argv[3:])
        info = corpus.get_corpus_db_detail(args.dataset_name)
        if info:
            print(info)
        else:
            print("Not found.")

    def catalog(self, argv):
        """Print dataset/corpus available for download."""
        corpus_db = corpus.get_corpus_db(corpus.corpus_db_url())
        corpus_db = corpus_db.json()
        corpus_names = sorted(corpus_db.keys())
        print("Dataset/corpus available for download:")
        for name in corpus_names:
            print(f"- {name} {corpus_db[name]['version']}", end="")
            corpus_info = corpus.get_corpus_db_detail(name)
            if corpus_info:
                print(f"  (Local: {corpus_info['version']})")
            else:
                print()

        print("\nUse subcommand 'get' to download dataset.")
        print("Example: thainlp data get crfcut")

    def path(self, argv):
        """Print path for local dataset."""
        print(get_pythainlp_data_path())
