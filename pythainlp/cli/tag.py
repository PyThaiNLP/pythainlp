# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Command line for PyThaiNLP's taggers.
"""
import argparse

from pythainlp import cli
from pythainlp.tag import pos_tag


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tag " + name))
        parser.add_argument(
            "text",
            type=str,
            help="input text",
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
        parser = argparse.ArgumentParser(
            prog="tag",
            description="Annotate a text with linguistic information",
            usage=(
                'thainlp tag <tag_type> [--sep "<separator>"] "<text>"\n\n'
                "tag_type:\n\n"
                "pos                part-of-speech\n\n"
                "<separator> and <text> should be inside double quotes.\n"
                "<text> should be a tokenized text, "
                "with tokens separated by <separator>.\n\n"
                "Example:\n\n"
                'thainlp tag pos -s " " "แรงดึงดูด เก็บ หัว คุณ ลง"\n\n'
                "--"
            ),
        )
        parser.add_argument("tag_type", type=str, help="[pos]")

        args = parser.parse_args(argv[2:3])
        cli.exit_if_empty(args.tag_type, parser)
        tag_type = str.lower(args.tag_type)

        argv = argv[3:]

        if tag_type == "pos":
            POSTaggingApp("Part-of-Speech tagging", argv)
        else:
            print(f"Tag type not available: {tag_type}")
