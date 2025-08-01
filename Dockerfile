# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

FROM python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libicu-dev  python3-pip python3-venv pkg-config && rm -rf /var/lib/apt/lists/*
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN if [ -f docker_requirements.txt ]; then pip install -r docker_requirements.txt; fi
RUN pip install -e .[full] && pip cache purge
