import logging
import os
from datetime import datetime
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import MagicMock, patch

import httpx
from fastapi import BackgroundTasks, FastAPI, Header, Response
from fastapi.testclient import TestClient
from httpx import AsyncClient

app = FastAPI()


@app.get("/{path_to_server:path}")
async def forward(
    path_to_server: str,
    background_tasks: BackgroundTasks,
    x_destination_host: str = Header(min_length=1),
) -> Response:
    start = datetime.now()
    async with AsyncClient() as client:
        response = await client.get(
            f"http://{x_destination_host}/{path_to_server}",
        )
    time_passed = (datetime.now() - start).total_seconds()
    record_time_metrix(time_passed, x_destination_host, path_to_server)
    return Response(content=response.content)


def record_time_metrix(
    time_used_in_secs: float,
    target: str,
    path: str,
):
    params = {
        "org": "brian",
        "bucket": "api",
        "precision": "s",
    }
    headers = {
        "Authorization": f"Bearer {os.environ.get('INFLUXDB_CONNECTION_TOKEN')}",
        "Content-Type": "text/plain; charset=utf-8",
        "Accept": "application/json",
    }
    content = (
        f"time,target={target},uri={path}"
        f" time_elapsed={time_used_in_secs}"
        f" {int(datetime.utcnow().timestamp())}"
    )
    response = httpx.post(
        "http://influxdb:8086/api/v2/write",
        params=params,
        headers=headers,
        data=content,
    )
    logging.critical(response.status_code)


class TestForward(TestCase):
    client = TestClient(app)

    @patch("proxy.AsyncClient", autospec=True)
    def test_forward(self, MockAsyncClient: MagicMock):
        dest = "saas"
        saas_response = b"content"
        instance = MockAsyncClient.return_value
        instance.__aenter__.return_value = instance
        instance.get.return_value.content = saas_response

        response = self.client.get(
            "/path/to/destination", headers={"x-destination-host": dest}
        )

        instance.get.assert_called_with("http://saas/path/to/destination")
        self.assertEqual(saas_response, response.content)

    def test_no_x_destination_header_will_get_429(self):
        response = self.client.get("/path")

        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
