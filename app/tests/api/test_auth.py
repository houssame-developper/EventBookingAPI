import pytest
from datetime import datetime, timezone
from tests.constants import user_create_factory


@pytest.mark.api
class TestAuthAPI:
    async def test_register_success(self, client):
        response = await client.post("/api/auth/register", json={
            "name": "Test User",
            "email": f"test_{datetime.now(timezone.utc).timestamp()}@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert "@example.com" in data["user"]["email"]

    async def test_register_duplicate_email(self, client, user_create_factory):
        email = f"dup_{datetime.now(timezone.utc).timestamp()}@example.com"
        await client.post("/api/auth/register", json={
            "name": "User A",
            "email": email,
            "password": "password123"
        })
        response = await client.post("/api/auth/register", json={
            "name": "User B",
            "email": email,
            "password": "password123"
        })
        assert response.status_code == 422
        assert "exists" in response.json()["detail"]

    async def test_login_success(self, client, user_create_factory):
        email = f"login_{datetime.now(timezone.utc).timestamp()}@example.com"
        await client.post("/api/auth/register", json={
            "name": "Login User",
            "email": email,
            "password": "password123"
        })
        response = await client.post("/api/auth/login", json={
            "email": email,
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data

    async def test_login_wrong_password(self, client, user_create_factory):
        email = f"wrongpass_{datetime.now(timezone.utc).timestamp()}@example.com"
        await client.post("/api/auth/register", json={
            "name": "Wrong Pass User",
            "email": email,
            "password": "password123"
        })
        response = await client.post("/api/auth/login", json={
            "email": email,
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    async def test_login_nonexistent_email(self, client):
        response = await client.post("/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "password123"
        })
        assert response.status_code == 422

    async def test_refresh_token_success(self, client):
        email = f"refresh_{datetime.now(timezone.utc).timestamp()}@example.com"
        register_resp = await client.post("/api/auth/register", json={
            "name": "Refresh User",
            "email": email,
            "password": "password123"
        })
        assert register_resp.status_code == 200
        refresh_token = register_resp.cookies.get("refresh_token")
        assert refresh_token is not None

        refresh_resp = await client.post("/api/auth/refresh", cookies={"refresh_token": refresh_token})
        assert refresh_resp.status_code == 200
        assert "access_token" in refresh_resp.json()

    async def test_refresh_token_missing(self, client):
        response = await client.post("/api/auth/refresh")
        assert response.status_code == 401

    async def test_logout(self, client):
        email = f"logout_{datetime.now(timezone.utc).timestamp()}@example.com"
        register_resp = await client.post("/api/auth/register", json={
            "name": "Logout User",
            "email": email,
            "password": "password123"
        })
        assert register_resp.status_code == 200

        logout_resp = await client.post("/api/auth/logout")
        assert logout_resp.status_code == 200
        assert logout_resp.json()["message"] == "Logout successfully"