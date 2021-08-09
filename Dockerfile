FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update -y && \
    apt-get install make curl -y && \
    apt-get clean -y && \
    apt-get install gdal-bin libgdal-dev python3-gdal -y && \
    pip install --upgrade pip &&\
    pip install poetry

COPY pyproject.toml ./

RUN poetry export -f requirements.txt --output requirements.txt

RUN pip install -r requirements.txt

RUN mkdir /var/log/app

COPY . /app

EXPOSE 8000