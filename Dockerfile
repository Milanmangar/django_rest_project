docker-machine regenerate-certs --client-certs
FROM python:3.8.2-alpine
MAINTAINER Milan Thapa

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D milan
User milan
