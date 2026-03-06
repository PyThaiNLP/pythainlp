# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Fuzzing harness for pythainlp.util.normalize()

This fuzzer tests the normalize function with random Unicode input
to discover edge cases, crashes, and potential security issues.
"""

import sys

import atheris

with atheris.instrument_imports():
    import pythainlp.util


def test_one_input(data: bytes) -> None:
    """Fuzz target for normalize.

    :param bytes data: Random input bytes from the fuzzer
    :rtype: None
    """
    fdp = atheris.FuzzedDataProvider(data)

    try:
        # Generate random Unicode string
        text = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())

        # Test normalize
        result = pythainlp.util.normalize(text)

        # Validate output type
        if not isinstance(result, str):
            raise TypeError(f"Expected str, got {type(result)}")

    except ValueError:
        # Expected exception - UnicodeDecodeError is a subclass of ValueError
        pass


def main() -> None:
    """Entry point for the fuzzer.

    :rtype: None
    """
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
