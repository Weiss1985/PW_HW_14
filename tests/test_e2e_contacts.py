
from operator import concat
import pytest

from unittest.mock import Mock, patch, AsyncMock

from src.services.auth import auth_service

test_concat = {
    "first_name": "bill" ,
    "second_name": "smith",
    "mail": "qwerty@i.ua",
    "birthday": "2000-03-07",
    "addition": "qwerty",
}


def test_get_contacts(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/", headers=headers)
        assert response.status_code == 404, response.text
        data = response.json()
        assert data.get("detail") == "Contact not found!"


def test_post_contacts(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts/", headers=headers, json=test_concat )
        response.text
        data = response.json()
        assert data["first_name"]  == test_concat["first_name"]
        assert data["second_name"] == test_concat["second_name"]
        assert data["mail"] == test_concat["mail"]
        assert data["birthday"] == test_concat["birthday"]
        assert data["addition"] == test_concat["addition"]


# def test_get_contacts(client, get_token, monkeypatch):
#     with patch.object(auth_service, 'cache') as redis_mock:
#         redis_mock.get.return_value = None
#         monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
#         monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
#         monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
#         token = get_token
#         headers = {"Authorization": f"Bearer {token}"}
#         response = client.get("api/contacts/all", headers=headers)
#         assert response.status_code == 404, response.text
#         data = response.json()
#         assert data.get("detail") == "Contact not found!"

