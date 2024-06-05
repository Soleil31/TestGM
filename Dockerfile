FROM python:3.12.2-slim

ENV POETRY_VERSION=1.8.2
ENV PYTHONUNBUFFERED 1

WORKDIR /TestGM

COPY . /TestGM

RUN python3 -m venv /opt/poetry-venv \
    && /opt/poetry-venv/bin/pip install -U pip setuptools \
    && /opt/poetry-venv/bin/pip install poetry==${POETRY_VERSION}
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

RUN /opt/poetry-venv/bin/poetry install --no-interaction --no-cache --no-root
RUN /opt/poetry-venv/bin/poetry self update
