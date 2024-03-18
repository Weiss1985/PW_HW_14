
from ast import LtE
from unittest.mock import Mock, patch, AsyncMock

import pytest # type: ignore
from sqlalchemy import select
from httpx import AsyncClient
from main import app
from fastapi.responses import FileResponse

from src.schemas.auth import TokenModel
from src.database.models import User
from tests.conftest import TestingSessionLocal


user_data = {"username": "john", "mail": "eva@i.ua", "password": "123456789"}


def test_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["mail"] == user_data["mail"]
    assert "password" not in data
    assert "avatar" in data
    assert mock_send_email.call_count == 1


def test_signup_exist_user(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] =="Account allready exist"


def test_login_not_confirmed(client, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.post("api/auth/login",
                           data={"username": user_data.get("mail"), "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


@pytest.mark.asyncio
async def test_login(client, monkeypatch):
    async with TestingSessionLocal() as session:
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        current_user = await session.execute(select(User).where(User.mail == user_data.get("mail")))
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            await session.commit()
    response = client.post("api/auth/login",
                           data={"username": user_data.get("mail"), 
                           "password": user_data.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


def test_login_wrong_password(client, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.post("api/auth/login",
                           data={"username": user_data.get("mail"), "password": "password"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid pass"


def test_login_wrong_email(client, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.post("api/auth/login",
                           data={"username": "mail", "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid user"


def test_login_validation_error(client, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.post("api/auth/login",
                           data={"password": user_data.get("password")})
    assert response.status_code == 422, response.text
    data = response.json()



def test_confirmed_email(client, get_token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    token = get_token
    response = client.get("api/auth/confirmed_email/" + token)
    response.text
    data = response.json()
    assert data["message"] == "Your email is already confirmed"




def test_get_request_mail(client, get_token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    token = get_token
    response = client.get(f"api/auth/{user_data.get('username')}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    # assert  isinstance(response, FileResponse)
    data = response.headers['content-length']
    assert data != 0


# def test_post_request_mail(client, get_token, monkeypatch):
#     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
#     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
#     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
#     token = get_token
#     response = client.get(f"api/auth/{user_data.get('username')}")
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "image/png"
#     # assert  isinstance(response, FileResponse)
#     data = response.headers['content-length']
#     assert data != 0










