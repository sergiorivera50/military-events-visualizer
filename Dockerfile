FROM python:3.6.9-alpine

RUN apk update && \
    apk add \
      build-base \
      curl

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
COPY ./inject.py ./inject.py
