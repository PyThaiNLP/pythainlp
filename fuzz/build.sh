#!/bin/bash -eu
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Build script for ClusterFuzzLite fuzzing harnesses
# This script installs atheris and prepares all fuzzing harnesses

echo "Building PyThaiNLP fuzz targets..."

# Install atheris for Python fuzzing with pinned version for security
pip install "atheris==2.3.0"

# Find all fuzz_*.py files in the fuzz directory
for fuzzer in "${SRC}/pythainlp/fuzz"/fuzz_*.py; do
    [[ -e "$fuzzer" ]] || continue
    fuzzer_basename=$(basename -s .py "$fuzzer")

    echo "Preparing ${fuzzer_basename}..."

    # Copy fuzzer to output directory (instrumentation happens at runtime)
    cp "${fuzzer}" "${OUT}/${fuzzer_basename}"

    # Make fuzzer executable
    chmod +x "${OUT}/${fuzzer_basename}"
done

echo "Build completed successfully!"
