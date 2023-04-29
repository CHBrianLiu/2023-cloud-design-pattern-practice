import json
from unittest import TestCase
from unittest.mock import patch, Mock

from azure.core.exceptions import ResourceExistsError
from linebot.models import TextMessage, MessageEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction

from . import handlers
from .. import az


class TestHandleWebhookWithRealAzureQueue(TestCase):
    @classmethod
    def setUp(cls) -> None:
        try:
            az.queue_client.create_queue()
        except ResourceExistsError:
            pass
        az.queue_client.clear_messages()

    def tearDown(self) -> None:
        az.queue_client.clear_messages()

    @patch.object(handlers.line_bot_api, "reply_message")
    def test_push_message_to_queue(self):
        content = "a message"
        event = MessageEvent(message=TextMessage(text=content))

        handlers.handle_text_message(event)
        message = az.queue_client.receive_message()
        queue_content = json.loads(message.content)["prompt"]

        self.assertEqual(queue_content, content)


class TestHandleTextMessageReply(TestCase):

    @patch.object(handlers.line_bot_api, "reply_message")
    @patch("uuid.uuid4")
    def test_reply_buttons_template(self, reply_method: Mock, fake_uuid_generator: Mock):
        fake_uuid_generator.return_value("uuid")
        reply_token = "reply_token"
        event = MessageEvent(
            message=TextMessage(text="a message"),
            reply_token=reply_token,
        )
        expected_reply_message = TemplateSendMessage(
            alt_text="Generating",
            template=ButtonsTemplate(
                text="Generating",
                actions=[
                    PostbackAction(
                        label="check",
                        display_text="Check",
                        data="uuid",
                    )
                ]
            )
        )

        handlers.handle_text_message(event)

        reply_method.assert_called_with(reply_token, expected_reply_message)
