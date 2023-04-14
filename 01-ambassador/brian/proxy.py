from http import HTTPStatus
from unittest import TestCase
from unittest.mock import MagicMock, patch

from fastapi import FastAPI, Header, Response
from fastapi.testclient import TestClient
from httpx import AsyncClient

app = FastAPI()


@app.get("/{path_to_server:path}")
async def forward(
    path_to_server: str, x_destination_host: str = Header(min_length=1)
) -> Response:
    async with AsyncClient() as client:
        response = await client.get(
            f"http://{x_destination_host}/{path_to_server}",
        )
    return Response(content=response.content)


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
