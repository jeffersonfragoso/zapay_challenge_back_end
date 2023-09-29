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
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0


# install system dependencies
RUN apt-get update && \
    apt-get install -y netcat && \
    pip install "poetry==$POETRY_VERSION"

FROM base AS dependencies_stage

WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM dependencies_stage as runtime

WORKDIR /usr/
ENV PYTHONPATH=${PYTHONPATH}/usr/src
COPY . /usr/
