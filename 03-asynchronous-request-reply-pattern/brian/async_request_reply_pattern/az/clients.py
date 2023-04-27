from azure.storage.queue import QueueClient
from azure.core.exceptions import ResourceExistsError

from . import constants


def create_queue_client():
    client = QueueClient.from_connection_string(
        (
            constants.AZ_STORAGE_ACCOUNT_CONNECTION_STRING
            if not constants.LOCAL
            else constants.AZ_DEV_STORAGE_ACCOUNT_CONNECTION_STRING
        ),
        constants.AZ_STORAGE_QUEUE_NAME,
    )
    return client

