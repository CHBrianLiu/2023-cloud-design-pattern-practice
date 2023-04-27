import json
import typing
import uuid

from fastapi import (
    FastAPI, Header, status, Request, HTTPException, BackgroundTasks
)
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent

from . import constants
from .line import BackgroundTaskWebhookHandler as WebhookHandler
from .. import az

app = FastAPI()

line_bot_api = LineBotApi(constants.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(constants.LINE_CHANNEL_SECRET)


class PromptMessage(typing.TypedDict):
    id: str
    prompt: str


@handler.add(MessageEvent, TextMessage)
def handle_text_message(event: MessageEvent):
    text_message: TextMessage = event.message
    queue_message: PromptMessage = {
        "id": str(uuid.uuid4()),
        "prompt": text_message.text,
    }
    az.queue_client.send_message(json.dumps(queue_message))


@app.post("/")
async def handle_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str | None = Header(default=None),
):
    body = (await request.body()).decode()

    try:
        handler.handle_background(background_tasks, body, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return
