from random import randint

from httpx import Client

saas_hosts = ["saas1", "saas2", "saas3"]
proxy_host = "proxy"


def main():
    with Client() as client:
        while True:
            target = saas_hosts[randint(0, len(saas_hosts) - 1)]
            response = client.get(
                f"http://{proxy_host}/hello",
                headers={"x-destination-host": target},
            )
            print(f"response from {target}: {response.content}")


if __name__ == "__main__":
    main()
