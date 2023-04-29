import json
import logging
import time

from azure.storage.queue import QueueMessage
from azure.storage.blob import BlobType
from . import constants
import openai

from .. import az
from ..models import PromptMessage


def retrieve_message() -> PromptMessage | None:
    message: QueueMessage | None = az.queue_client.receive_message()
    if message is None:
        return None
    return json.loads(message.content)


def generate_picture(prompt: str) -> str:
    response = openai.Image.create(
        api_key=constants.OPENAPI_API_KEY,
        prompt=prompt,
    )
    return response["data"][0]["url"]


def upload_blob(filename: str, content: str):
    az.container_client.upload_blob(
        filename,
        content,
        BlobType.BLOCKBLOB,
    )


def main():
    while True:
        try:
            message = retrieve_message()
            if message is None:
                time.sleep(5)
                continue

            pic_url = generate_picture(message["prompt"])
            upload_blob(message["id"], pic_url)
        except Exception as e:
            logging.error("exception occurred: %s", e)
