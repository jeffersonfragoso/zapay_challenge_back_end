# pull official base image
FROM python:3.11.4-slim-buster as base

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=10000 \
    POETRY_VERSION=1.6.1


# install system dependencies
RUN apt-get update && apt-get install -y netcat

FROM base AS dependencies_stage

WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock /tmp/

RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

FROM dependencies_stage

WORKDIR /usr/

ENV PYTHONPATH=${PYTHONPATH}/usr/src

COPY . /usr/
RUN poetry install --only-root
