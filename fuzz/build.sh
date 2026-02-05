#!/bin/bash -eu
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileType: SOURCE

# Build script for ClusterFuzzLite fuzzing harnesses
# This script installs atheris and compiles all fuzzing harnesses

echo "Building PyThaiNLP fuzz targets..."

# Install atheris for Python fuzzing
pip install atheris

# Find all fuzz_*.py files in the fuzz directory
for fuzzer in "${SRC}/pythainlp/fuzz"/fuzz_*.py; do
    fuzzer_basename=$(basename -s .py "$fuzzer")
    fuzzer_package="fuzz.${fuzzer_basename}"

    echo "Compiling ${fuzzer_basename}..."

    # Compile fuzzer with atheris
    python -m atheris.instrument_libfuzzer "${fuzzer}" "${OUT}/${fuzzer_basename}"

    # Make fuzzer executable
    chmod +x "${OUT}/${fuzzer_basename}"
done

echo "Build completed successfully!"
