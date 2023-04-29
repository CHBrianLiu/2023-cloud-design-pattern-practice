import json
import time
from unittest import TestCase, skipIf
from unittest.mock import patch
import os

from fastapi.testclient import TestClient
from linebot.exceptions import InvalidSignatureError
from azure.core.exceptions import ResourceExistsError

from . import main
from . import handlers
from .. import az


class TestHandleWebhook(TestCase):
    client = TestClient(main.app)

    def test_handle_webhook_return_400_for_invalid_signature(self):
        with patch.object(
            handlers.handler.parser.signature_validator,
            "validate",
            autospec=True
        ) as mock_validate:
            mock_validate.side_effect = InvalidSignatureError

            response = self.client.post(
                "/",
                headers={"X-Line_Signature": "invalid"},
            )

            self.assertEqual(response.status_code, 400)

    def test_handle_webhook_call_func_in_the_background(self):
        with patch.object(
            main,
            "az",
            autospec=True
        ) as az, patch.object(
            handlers.handler.parser.signature_validator,
            "validate",
            autospec=True
        ):
            event = {
                "destination": "xxxxxxxxxx",
                "events": [
                    {
                        "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
                        "type": "message",
                        "mode": "active",
                        "timestamp": 1462629479859,
                        "source": {
                            "type": "group",
                            "groupId": "Ca56f94637c...",
                            "userId": "U4af4980629..."
                        },
                        "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                        "deliveryContext": {
                            "isRedelivery": False
                        },
                        "message": {
                            "id": "444573844083572737",
                            "type": "text",
                            "text": "@All @example Good Morning!! (love)",
                        }
                    }
                ]
            }

            response = self.client.post(
                "/", headers={"X-Line_Signature": "valid"}, json=event
            )
            self.assertEqual(response.status_code, 200)

            time.sleep(1)
            az.queue_client.send_message.assert_called()



@skipIf(not os.environ.get("e2e_test"), "not e2e test")
class TestImageGenerationWorkflow(TestCase):
    client = TestClient(main.app)

    @classmethod
    def setUp(cls) -> None:
        try:
            az.queue_client.create_queue()
        except ResourceExistsError:
            pass
        try:
            az.container_client.create_container()
        except ResourceExistsError:
            pass
        az.queue_client.clear_messages()

    def test_send_message_to_generate_image(self):
        with patch.object(
            handlers.handler.parser.signature_validator,
            "validate",
            autospec=True
        ), patch("uuid.uuid4") as fake_uuid4:
            fake_uuid4.return_value = "uuid"
            event = {
                "destination": "xxxxxxxxxx",
                "events": [
                    {
                        "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
                        "type": "message",
                        "mode": "active",
                        "timestamp": 1462629479859,
                        "source": {
                            "type": "group",
                            "groupId": "Ca56f94637c...",
                            "userId": "U4af4980629..."
                        },
                        "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                        "deliveryContext": {
                            "isRedelivery": False
                        },
                        "message": {
                            "id": "444573844083572737",
                            "type": "text",
                            "text": "A polar bear doing bouldering.",
                        }
                    }
                ]
            }

            self.client.post(
                "/", headers={"X-Line_Signature": "valid"}, json=event
            )
            time.sleep(20)

            blob = az.container_client.get_blob_client("uuid")
            self.assertTrue(blob.exists())
            self.assertTrue(blob.download_blob().readall().startswith("https"))
