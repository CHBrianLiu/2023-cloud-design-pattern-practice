FROM python:3.11 AS base

COPY requirements.txt /app/requirements.txt

RUN pip install -U pip
RUN pip install -r /app/requirements.txt

FROM base AS db_manager

WORKDIR /app

COPY gen gen
COPY models models
COPY setup setup
COPY db_manager.py db_manager.py

ENV PYTHONPATH=/app/gen

#CMD ["python", "db_manager.py"]