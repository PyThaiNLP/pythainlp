# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Fuzzing harness for pythainlp.tokenize.word_tokenize()

This fuzzer tests the word_tokenize function with random Unicode input
to discover edge cases, crashes, and potential security issues.
"""

import sys

import atheris

import pythainlp.tokenize


def TestOneInput(data: bytes) -> None:
    """Fuzz target for word_tokenize.

    :param bytes data: Random input bytes from the fuzzer
    :rtype: None
    """
    fdp = atheris.FuzzedDataProvider(data)

    try:
        # Generate random Unicode string
        text = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())

        # Test word_tokenize with default engine
        result = pythainlp.tokenize.word_tokenize(text)

        # Validate output type
        if not isinstance(result, list):
            raise TypeError(f"Expected list, got {type(result)}")
        if not all(isinstance(token, str) for token in result):
            raise TypeError("All tokens should be strings")

    except (ValueError, TypeError, UnicodeDecodeError):
        # Expected exceptions - these are acceptable
        pass


def main() -> None:
    """Entry point for the fuzzer.
    
    :rtype: None
    """
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
