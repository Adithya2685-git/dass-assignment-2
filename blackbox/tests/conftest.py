import os

import pytest
import requests


BASE_URL = os.getenv("QUICKCART_BASE_URL", "http://127.0.0.1:8080")
ROLL_NUMBER = os.getenv("QUICKCART_ROLL_NUMBER", "2025000")
USER_ID = os.getenv("QUICKCART_USER_ID", "1")


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def session() -> requests.Session:
    return requests.Session()


@pytest.fixture(scope="session")
def admin_headers() -> dict[str, str]:
    return {"X-Roll-Number": ROLL_NUMBER}


@pytest.fixture(scope="session")
def user_headers(admin_headers: dict[str, str]) -> dict[str, str]:
    headers = dict(admin_headers)
    headers["X-User-ID"] = USER_ID
    return headers
