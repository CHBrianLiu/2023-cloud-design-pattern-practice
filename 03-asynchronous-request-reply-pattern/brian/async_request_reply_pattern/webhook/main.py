from fastapi import (
    FastAPI, Header, status, Request, HTTPException, BackgroundTasks
)
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError

from . import constants
from . import handlers

app = FastAPI()

line_bot_api = LineBotApi(constants.LINE_CHANNEL_ACCESS_TOKEN)


@app.post("/")
async def handle_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str | None = Header(default=None),
):
    body = (await request.body()).decode()

    try:
        handlers.handler.handle_background(
            background_tasks, body, x_line_signature
        )
    except InvalidSignatureError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return
