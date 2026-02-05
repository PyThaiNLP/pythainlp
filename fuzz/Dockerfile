# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileType: SOURCE

# Dockerfile for ClusterFuzzLite fuzzing
# This extends the OSS-Fuzz base builder image for Python projects

FROM gcr.io/oss-fuzz-base/base-builder-python

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libicu-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy repository to $SRC/pythainlp
COPY . $SRC/pythainlp

# Set working directory
WORKDIR $SRC/pythainlp

# Install pythainlp in development mode with minimal dependencies
# This installs the package without heavy ML dependencies to speed up builds
RUN pip install --no-cache-dir -e .

# Copy build script to $SRC/build.sh as expected by OSS-Fuzz/ClusterFuzzLite
COPY fuzz/build.sh $SRC/
