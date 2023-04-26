from fastapi import FastAPI, Header, status, Request, HTTPException, BackgroundTasks
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent

import constants
from line import BackgroundTaskWebhookHandler as WebhookHandler

app = FastAPI()

line_bot_api = LineBotApi(constants.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(constants.LINE_CHANNEL_SECRET)


def dummy_func():
    """Used in unit test to ensure event handlers are called in the background"""
    pass


@handler.add(MessageEvent, TextMessage)
def handle_text_message(event: MessageEvent):
    # message: TextMessage = event.message
    dummy_func()


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
