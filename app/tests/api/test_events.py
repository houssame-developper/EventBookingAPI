import pytest
from datetime import datetime, timezone


@pytest.mark.api
class TestEventAPI:
    async def test_create_event_as_admin(self, client, admin_headers):
        response = await client.post("/api/events", json={
            "title": "Test Event",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Test Event"

    async def test_create_event_as_regular_user(self, client, regular_headers):
        response = await client.post("/api/events", json={
            "title": "Test Event",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=regular_headers)
        assert response.status_code == 403

    async def test_list_events_public(self, client):
        response = await client.get("/api/events")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_event_public(self, client, admin_headers):
        create_resp = await client.post("/api/events", json={
            "title": "Public Event",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        event_id = create_resp.json()["id"]

        response = await client.get(f"/api/events/{event_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Public Event"

    async def test_update_event_as_admin(self, client, admin_headers):
        create_resp = await client.post("/api/events", json={
            "title": "Updatable Event",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        event_id = create_resp.json()["id"]

        response = await client.patch(f"/api/events/{event_id}", json={
            "title": "Updated Event"
        }, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Event"

    async def test_delete_event_as_admin(self, client, admin_headers):
        create_resp = await client.post("/api/events", json={
            "title": "Deletable Event",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        event_id = create_resp.json()["id"]

        response = await client.delete(f"/api/events/{event_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["message"] == "event deleted successfully"

    async def test_get_event_slots(self, client, admin_headers, regular_headers):
        create_resp = await client.post("/api/events", json={
            "title": "Slot Event",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        event_id = create_resp.json()["id"]

        await client.post(f"/api/events/{event_id}/bookings", headers=regular_headers)

        response = await client.get(f"/api/events/{event_id}/slots")
        assert response.status_code == 200
        assert response.json()["reserved_slots"] == 1

    async def test_create_booking_authenticated(self, client, admin_headers, regular_headers):
        create_resp = await client.post("/api/events", json={
            "title": "Bookable Event",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        event_id = create_resp.json()["id"]

        response = await client.post(f"/api/events/{event_id}/bookings", headers=regular_headers)
        assert response.status_code == 200
        assert response.json()["event_id"] == event_id

    async def test_create_booking_unauthorized(self, client, admin_headers):
        create_resp = await client.post("/api/events", json={
            "title": "Bookable Event 2",
            "description": "A test event description that is long enough for validation",
            "date": datetime.now(timezone.utc).isoformat(),
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        event_id = create_resp.json()["id"]

        response = await client.post(f"/api/events/{event_id}/bookings")
        assert response.status_code == 401