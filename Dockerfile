# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

FROM python:3.10-slim

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libicu-dev libicu63 pkg-config && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade "pip==24.0" "setuptools"
RUN if [ -f docker_requirements.txt ]; then pip3 install -r docker_requirements.txt; fi
RUN pip3 install -e .[full] && pip3 cache purge
