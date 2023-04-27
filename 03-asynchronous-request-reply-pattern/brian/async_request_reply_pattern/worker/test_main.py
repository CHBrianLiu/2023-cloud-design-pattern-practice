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
        main.upload_blob("test.txt", b"bytes")

        blob = az.container_client.get_blob_client("test.txt")

        self.assertTrue(blob.exists)


if __name__ == '__main__':
    unittest.main()
