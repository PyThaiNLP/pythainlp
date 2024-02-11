# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Command line for PyThaiNLP's dataset/corpus management.
"""
import argparse

from pythainlp import corpus
from pythainlp.tools import get_pythainlp_data_path


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            prog="data",
            description="Manage dataset/corpus.",
            usage=(
                "thainlp data <subcommand>\n\n"
                "subcommands:\n\n"
                "catalog                show list of available datasets\n"
                "info <dataset_name>    show information about the dataset\n"
                "get <dataset_name>     download the dataset\n"
                "rm <dataset_name>      remove the dataset\n"
                "path                   show full path to data directory\n\n"
                "Example:\n\n"
                "thainlp data get thai2fit_wv\n\n"
                "Current data path:\n\n"
                f"{get_pythainlp_data_path()}\n\n"
                "To change PyThaiNLP data path, set the operating system's\n"
                "PYTHAINLP_DATA_DIR environment variable.\n\n"
                "For more information about corpora that PyThaiNLP use, see:\n"
                "https://github.com/PyThaiNLP/pythainlp-corpus/\n\n"
                "--"
            ),
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
            "dataset_name",
            type=str,
            help="dataset/corpus's name",
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
            "dataset_name",
            type=str,
            help="dataset/corpus's name",
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
            "dataset_name",
            type=str,
            help="dataset/corpus's name",
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
            print(f"- {name} {corpus_db[name]['latest_version']}", end="")
            corpus_info = corpus.get_corpus_db_detail(name)
            if corpus_info:
                print(f"  (Local: {corpus_info['version']})")
            else:
                print()

        print(
            "\nUse subcommand 'get' to download a dataset.\n\n"
            "Example: thainlp data get crfcut\n"
        )

    def path(self, argv):
        """Print path of local dataset."""
        print(get_pythainlp_data_path())
