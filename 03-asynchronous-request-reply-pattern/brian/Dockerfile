FROM python:3.11 AS dev

RUN pip install -U pip

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY async_request_reply_pattern /app/async_request_reply_pattern

FROM dev AS webhook

CMD ["uvicorn", "async_request_reply_pattern.webhook.main:app", "--host", "0.0.0.0", "--port", "80"]
