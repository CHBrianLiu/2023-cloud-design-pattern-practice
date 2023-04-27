from azure.storage.queue import QueueClient
from azure.storage.blob import ContainerClient

from . import constants

connection_string = (
    constants.AZ_STORAGE_ACCOUNT_CONNECTION_STRING
    if not constants.LOCAL
    else constants.AZ_DEV_STORAGE_ACCOUNT_CONNECTION_STRING
)


def create_queue_client():
    client = QueueClient.from_connection_string(
        connection_string,
        constants.AZ_STORAGE_QUEUE_NAME,
    )
    return client


def create_container_client():
    return ContainerClient.from_connection_string(
        connection_string,
        constants.AZ_STORAGE_BLOB_CONTAINER_NAME,
    )
