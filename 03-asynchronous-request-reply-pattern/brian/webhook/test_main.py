import time
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient
from linebot.models import MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError

import main


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

    def test_handle_webhook_call_dummy_func_in_the_background(self):
        with patch.object(
            main,
            "dummy_func",
            autospec=True
        ) as dummy_func, patch.object(
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
            dummy_func.assert_called()
