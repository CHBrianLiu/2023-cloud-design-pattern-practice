import json
import unittest

from azure.core.exceptions import ResourceExistsError

from . import main
from .. import az


class TestUploadBlobToRealAzureBlob(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            az.container_client.create_container()
        except ResourceExistsError:
            pass

    def test_upload_blob(self):
        main.upload_blob("test.txt", "bytes")

        blob = az.container_client.get_blob_client("test.txt")

        self.assertTrue(blob.exists)


class TestRetrieveMessageWithRealAzureQueue(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        try:
            az.queue_client.create_queue()
        except ResourceExistsError:
            pass
        az.queue_client.clear_messages()

    def test_retrieve_message_from_queue(self):
        queue_message = {
            "id": "id",
            "prompt": "prompt"
        }
        az.queue_client.send_message(json.dumps(queue_message))

        message = main.retrieve_message()

        self.assertEqual(message, queue_message)

    def test_retrieve_message_from_empty_queue(self):
        message = main.retrieve_message()

        self.assertIsNone(message)
