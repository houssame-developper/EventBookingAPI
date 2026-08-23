import pytest
from datetime import datetime, timezone


@pytest.mark.api
class TestUserAPI:
    async def test_create_user_as_admin(self, client, admin_headers):
        response = await client.post("/api/users", json={
            "name": "New User",
            "email": f"newuser_{datetime.now(timezone.utc).timestamp()}@example.com",
            "password": "password123",
            "role": "user"
        }, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["email"].startswith("newuser_")

    async def test_create_user_as_regular_user(self, client, regular_headers):
        response = await client.post("/api/users", json={
            "name": "New User",
            "email": f"newuser2_{datetime.now(timezone.utc).timestamp()}@example.com",
            "password": "password123"
        }, headers=regular_headers)
        assert response.status_code == 403

    async def test_get_me(self, client, regular_headers):
        response = await client.get("/api/users/me", headers=regular_headers)
        assert response.status_code == 200
        assert "email" in response.json()

    async def test_get_me_unauthorized(self, client):
        response = await client.get("/api/users/me")
        assert response.status_code == 401

    async def test_list_users_as_admin(self, client, admin_headers):
        response = await client.get("/api/users", headers=admin_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_list_users_as_regular_user(self, client, regular_headers):
        response = await client.get("/api/users", headers=regular_headers)
        assert response.status_code == 403

    async def test_get_user_as_admin(self, client, admin_headers, regular_headers):
        me_resp = await client.get("/api/users/me", headers=regular_headers)
        user_id = me_resp.json()["id"]

        response = await client.get(f"/api/users/{user_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    async def test_update_user_as_admin(self, client, admin_headers, regular_headers):
        me_resp = await client.get("/api/users/me", headers=regular_headers)
        user_id = me_resp.json()["id"]

        response = await client.patch(f"/api/users/{user_id}", json={
            "name": "Updated Name"
        }, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    async def test_delete_user_as_admin(self, client, admin_headers, regular_headers):
        me_resp = await client.get("/api/users/me", headers=regular_headers)
        user_id = me_resp.json()["id"]

        response = await client.delete(f"/api/users/{user_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["message"] == "user deleted successfully"