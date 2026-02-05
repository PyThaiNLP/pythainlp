#!/bin/bash -eu
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileType: SOURCE

# Build script for ClusterFuzzLite fuzzing harnesses
# This script installs atheris and prepares all fuzzing harnesses

echo "Building PyThaiNLP fuzz targets..."

# Install atheris for Python fuzzing with version constraint
pip install "atheris>=2.3.0"

# Find all fuzz_*.py files in the fuzz directory
for fuzzer in "${SRC}/pythainlp/fuzz"/fuzz_*.py; do
    fuzzer_basename=$(basename -s .py "$fuzzer")

    echo "Preparing ${fuzzer_basename}..."

    # Copy fuzzer to output directory (instrumentation happens at runtime)
    cp "${fuzzer}" "${OUT}/${fuzzer_basename}"

    # Make fuzzer executable
    chmod +x "${OUT}/${fuzzer_basename}"
done

echo "Build completed successfully!"
