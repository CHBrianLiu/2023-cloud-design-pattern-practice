from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.storage.blob import ContainerClient

from . import constants

connection_string = (
    constants.AZ_STORAGE_ACCOUNT_CONNECTION_STRING
    if not constants.LOCAL
    else constants.AZ_DEV_STORAGE_ACCOUNT_CONNECTION_STRING
)


def create_queue_client():
    if connection_string:
        client = QueueClient.from_connection_string(
            connection_string,
            constants.AZ_STORAGE_QUEUE_NAME,
        )
    else:
        credential = DefaultAzureCredential()
        client = QueueClient(
            f"https://{constants.AZ_STORAGE_ACCOUNT_NAME}.table.core.windows.net/",
            constants.AZ_STORAGE_QUEUE_NAME,
            credential,
        )
    return client


def create_container_client():
    if connection_string:
        client = ContainerClient.from_connection_string(
            connection_string,
            constants.AZ_STORAGE_BLOB_CONTAINER_NAME,
        )
    else:
        credential = DefaultAzureCredential()
        client = ContainerClient(
            f"https://{constants.AZ_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/",
            constants.AZ_STORAGE_BLOB_CONTAINER_NAME,
            credential,
        )
    return client
