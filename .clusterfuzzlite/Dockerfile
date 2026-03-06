# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Dockerfile for ClusterFuzzLite fuzzing.
# ClusterFuzzLite requires this file at .clusterfuzzlite/Dockerfile.
# This extends the OSS-Fuzz base builder image for Python projects.

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

# Install pythainlp as a regular install so PyInstaller can bundle it
# Editable installs use path hooks that PyInstaller cannot follow
RUN pip install --no-cache-dir .

# Copy build script to $SRC/build.sh as expected by OSS-Fuzz/ClusterFuzzLite
COPY .clusterfuzzlite/build.sh $SRC/
