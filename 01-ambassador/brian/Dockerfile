# base layer
FROM python:3.11 AS base

## add workspace folder
RUN mkdir /app
WORKDIR /app

## install all dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# fake saas app
FROM base AS saas

COPY ./saas.py /app/saas.py

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "80", "saas:app" ]

