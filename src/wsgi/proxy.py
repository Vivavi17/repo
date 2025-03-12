import json

import requests


def app(environ, start_response):
    path = environ.get("PATH_INFO").strip("/")
    data = get_response(path)
    status = "200 OK"
    response_headers = [
        ("Content-type", "application/json"),
    ]
    start_response(status, response_headers)
    return [json.dumps(data).encode("utf-8")]


def get_response(currency: str) -> dict | None:
    if not currency:
        return
    try:
        response = requests.get(
            f"https://api.exchangerate-api.com/v4/latest/{currency}"
        )
    except Exception:
        return
    if response.status_code == 200:
        return response.json()
