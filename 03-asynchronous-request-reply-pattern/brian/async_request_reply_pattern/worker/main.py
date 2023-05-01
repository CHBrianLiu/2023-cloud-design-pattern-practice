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
    raw_message: QueueMessage | None = az.queue_client.receive_message()
    if raw_message is None:
        return None
    message = json.loads(raw_message.content)
    az.queue_client.delete_message(raw_message)
    return message


def generate_picture(prompt: str) -> str:
    response = openai.Image.create(
        api_key=constants.OPENAI_API_KEY,
        prompt=prompt,
    )
    return response["data"][0]["url"]

def blob_exists(filename: str) -> bool:
    return az.container_client.get_blob_client(filename).exists()

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
                logging.info("No message left in the queue. Sleeping...")
                time.sleep(10)
                continue
            # check blob existence first to avoid redundant calls
            if blob_exists(message["id"]):
                logging.warning("Duplicate work. Skipping...")
                continue

            pic_url = generate_picture(message["prompt"])
            upload_blob(message["id"], pic_url)
        except Exception as e:
            logging.error("exception occurred: %s", e)
