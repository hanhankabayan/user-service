import httpx


class HttpClient:
    client = httpx.AsyncClient(
        timeout=60,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )
