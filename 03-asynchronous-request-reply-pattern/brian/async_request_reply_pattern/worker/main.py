from azure.storage.blob import BlobType
from .. import az


def upload_blob(filename: str, content: bytes):
    az.container_client.upload_blob(
        filename,
        content,
        BlobType.BLOCKBLOB,
    )