FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && \
    apt install -y python3-dev

RUN pip install --upgrade pip

EXPOSE 8000

COPY . .
