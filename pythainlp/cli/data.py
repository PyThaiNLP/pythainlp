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
            # choices=["catalog", "info", "get", "rm", "path", "ls"],
            help="action on dataset/corpus (catalog, info, download, remove, path)",
        )

        args = parser.parse_args(argv[2:3])
        if not hasattr(App, args.subcommand):
            print(f"Subcommand not available: {args.subcommand}")
            parser.print_help()
            exit(1)

        getattr(self, args.subcommand)(argv)

    def download(self, argv):
        parser = argparse.ArgumentParser(
            description="Download dataset",
            usage="thainlp data download <dataset_name>",
        )
        parser.add_argument(
            "dataset_name", type=str, help="dataset/corpus's name",
        )
        args = parser.parse_args(argv[3:])
        if corpus.download(args.dataset_name):
            print("Downloaded successfully.")
        else:
            print("Not found.")

    def remove(self, argv):
        parser = argparse.ArgumentParser(
            description="Remove dataset",
            usage="thainlp data remove <dataset_name>",
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
            description="Dataset info",
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
            print("-", name, corpus_db[name]["version"])
        print("\nUse subcommand 'download' to download dataset.")
        print("example: thainlp data download crfcut")

    def path(self, argv):
        """Print path for local dataset."""
        print(get_pythainlp_data_path())
