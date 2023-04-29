import json
import uuid

from linebot.models import TextMessage, MessageEvent

from . import constants
from .line import BackgroundTaskWebhookHandler as WebhookHandler
from .. import az
from ..models import PromptMessage

handler = WebhookHandler(constants.LINE_CHANNEL_SECRET)


@handler.add(MessageEvent, TextMessage)
def handle_text_message(event: MessageEvent):
    text_message: TextMessage = event.message
    queue_message: PromptMessage = {
        "id": str(uuid.uuid4()),
        "prompt": text_message.text,
    }
    az.queue_client.send_message(json.dumps(queue_message))
