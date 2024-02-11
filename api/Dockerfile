FROM python:3.10

WORKDIR /code

ENV POETRY_VIRTUALENVS_CREATE 0
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get upgrade -y
RUN apt install build-essential -y --no-install-recommends

COPY poetry.lock ./pyproject.toml /code/

RUN pip3 install poetry
RUN poetry install

COPY .. .

