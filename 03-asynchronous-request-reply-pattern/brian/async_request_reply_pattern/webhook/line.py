from linebot import WebhookHandler
from fastapi import BackgroundTasks


class BackgroundTaskWebhookHandler(WebhookHandler):
    def handle_background(
        self,
        background_tasks: BackgroundTasks,
        body: str,
        signature: str,
    ):
        """Make webhook handling tasks run after returning response.

        Before add a background work, validate the signature first.
        """
        self.parser.signature_validator.validate(body, signature)
        background_tasks.add_task(
            self.handle, body, signature,
        )
