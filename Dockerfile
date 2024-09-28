FROM python:3.12-slim

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install --no-install-recommends -y \
  vim \
  curl

ENV PATH="$PATH:/root/.local/bin"

RUN pip install pipx
RUN pipx install poetry
RUN pipx ensurepath

RUN mkdir /project
ADD . /project/
WORKDIR /project/

RUN poetry config virtualenvs.create false
RUN poetry install
