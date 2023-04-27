import json
import time
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from azure.core.exceptions import ResourceExistsError

from . import main
from .. import az


class TestHandleWebhook(TestCase):
    client = TestClient(main.app)

    def test_handle_webhook_return_400_for_invalid_signature(self):
        with patch.object(
            main.handler.parser.signature_validator,
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
            main.handler.parser.signature_validator,
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


class TestHandleWebhookWithRealAzureQueue(TestCase):
    client = TestClient(main.app)

    def setUp(self) -> None:
        try:
            az.queue_client.create_queue()
        except ResourceExistsError:
            pass

    def test_push_message_to_queue(self):
        content = "a message"
        event = MessageEvent(message=TextMessage(text=content))

        main.handle_text_message(event)
        message = az.queue_client.receive_message()
        queue_content = json.loads(message.content)["prompt"]

        self.assertEqual(queue_content, content)
