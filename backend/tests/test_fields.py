from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routes.fields import router
from . import run_migrations

app = FastAPI()
app.include_router(router)


def setup_module(module):
    # Reset database for tests
    run_migrations()


def test_field_booking_flow():
    client = TestClient(app)
    # create field
    res = client.post(
        "/fields",
        json={"name": "Central Park", "location": "NYC", "price_per_hour": 50.0},
    )
    assert res.status_code == 200
    field = res.json()

    # list fields
    res = client.get("/fields")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # book field
    booking_payload = {
        "start_time": "2024-01-01T10:00:00Z",
        "end_time": "2024-01-01T11:00:00Z",
        "provider": "stripe",
    }
    res = client.post(f"/fields/{field['id']}/bookings", json=booking_payload)
    assert res.status_code == 200
    booking = res.json()
    assert booking["paid"] is True
    assert booking["payment_id"].startswith("stripe_")

