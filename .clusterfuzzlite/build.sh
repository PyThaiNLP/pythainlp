#!/bin/bash -eu
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Build script for ClusterFuzzLite fuzzing harnesses.
# ClusterFuzzLite requires this file at .clusterfuzzlite/build.sh.
# This script installs atheris and prepares all fuzzing harnesses.

echo "Building PyThaiNLP fuzz targets..."

# Install atheris for Python fuzzing with pinned version for security
pip install "atheris==2.3.0"

# Find all fuzz_*.py files in the fuzz directory
for fuzzer in "${SRC}/pythainlp/fuzz"/fuzz_*.py; do
    [[ -e "$fuzzer" ]] || continue
    echo "Compiling $(basename "${fuzzer}")..."
    # compile_python_fuzzer creates a proper executable wrapper for libFuzzer
    compile_python_fuzzer "${fuzzer}"
done

echo "Build completed successfully!"
