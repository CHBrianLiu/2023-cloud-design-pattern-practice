from random import randint
from time import sleep

from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello():
    wait_secs = randint(0, 3)
    sleep(wait_secs)
    return {"Hello": "World"}
