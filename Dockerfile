FROM python:3.12.0-slim

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/python/.local/bin:${PATH}"

RUN apt-get update && \
    apt-get -y install  pkg-config default-libmysqlclient-dev \
        build-essential libmariadb-dev

RUN pip install --upgrade pip==24.2\
    && pip install pipenv==2024.0.1 flake8==6.1.0

COPY Pipfile Pipfile.lock /kafka/
RUN cd /kafka\
    && pipenv install --system --deploy

WORKDIR /kafka
COPY . /kafka/
