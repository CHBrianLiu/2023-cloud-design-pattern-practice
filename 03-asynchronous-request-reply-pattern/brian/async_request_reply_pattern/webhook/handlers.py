import enum
import json
import uuid

from linebot.models import TextMessage, MessageEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction, PostbackEvent, TextSendMessage

from . import constants
from .line import BackgroundTaskWebhookHandler as WebhookHandler, line_bot_api
from .. import az
from ..models import PromptMessage

handler = WebhookHandler(constants.LINE_CHANNEL_SECRET)


class CheckMessageStage(enum.StrEnum):
    INITIAL = "Generating..."
    CONSTANT = "In progress..."


def _compose_check_later_message(stage: CheckMessageStage, task_id: str):
    return TemplateSendMessage(
        alt_text=str(stage),
        template=ButtonsTemplate(
            text=str(stage),
            actions=[
                PostbackAction(
                    label="check",
                    display_text="Check",
                    data=task_id,
                )
            ]
        )
    )


@handler.add(MessageEvent, TextMessage)
def handle_text_message(event: MessageEvent):
    text_message: TextMessage = event.message
    task_id = str(uuid.uuid4())
    queue_message: PromptMessage = {
        "id": task_id,
        "prompt": text_message.text,
    }
    az.queue_client.send_message(json.dumps(queue_message))
    line_bot_api.reply_message(
        event.reply_token,
        _compose_check_later_message(CheckMessageStage.INITIAL, task_id)
    )

@handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):
    blob = az.container_client.get_blob_client(event.postback.data)
    if not blob.exists():
        line_bot_api.reply_message(
            event.reply_token,
            _compose_check_later_message(
                CheckMessageStage.CONSTANT,
                event.postback.data,
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(blob.download_blob().readall().decode())
        )