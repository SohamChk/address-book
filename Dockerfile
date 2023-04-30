FROM python:3.10-alpine3.14

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /address_book

ADD requirements.txt .

RUN set -ex \
    && apk add --no-cache build-base \
    gcc \
    musl-dev \
    python3-dev \
    libspatialite \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

ADD . .