FROM python:3.11

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./saas.py /app/saas.py

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "80", "saas:app" ]

