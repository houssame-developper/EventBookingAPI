import pytest
from datetime import datetime, timezone


@pytest.mark.api
class TestBookingAPI:
    async def test_my_bookings(self, client, admin_headers, regular_headers):
        create_resp = await client.post("/api/events", json={
            "title": "My Bookings Event",
            "description": "A test event description that is long enough for validation",
            "date": "2026-12-31T12:00:00+00:00",
            "total_slots": 10,
            "reserved_slots": 0
        }, headers=admin_headers)
        event_id = create_resp.json()["id"]

        await client.post(f"/api/events/{event_id}/bookings", headers=regular_headers)

        response = await client.get("/api/bookings/me", headers=regular_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1

    async def test_my_bookings_unauthorized(self, client):
        response = await client.get("/api/bookings/me")
        assert response.status_code == 401