FROM python:3.11 AS base

COPY requirements.txt /app/requirements.txt

RUN pip install -U pip
RUN pip install -r /app/requirements.txt

FROM base AS db_manager

WORKDIR /app

COPY models /app/models
COPY setup /app/setup
COPY db_manager.py /app/db_manager.py