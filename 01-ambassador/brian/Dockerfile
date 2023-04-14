# base layer
FROM python:3.11 AS base

## add workspace folder
RUN mkdir /app
WORKDIR /app

## install all dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# base fastapi server
FROM base AS base-fastapi-server

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "80", "main:app" ]

# fake saas app
FROM base-fastapi-server AS saas

COPY ./saas.py /app/main.py


# proxy to log response time
FROM base-fastapi-server AS proxy

COPY ./proxy.py /app/main.py

