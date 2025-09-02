def test_field_booking_flow(client):
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


def test_booking_conflict_validation(client):
    res = client.post(
        "/fields",
        json={"name": "Downtown", "location": "NYC", "price_per_hour": 75.0},
    )
    assert res.status_code == 200
    field = res.json()

    booking_payload = {
        "start_time": "2024-02-01T10:00:00Z",
        "end_time": "2024-02-01T11:00:00Z",
        "provider": "stripe",
    }
    res = client.post(f"/fields/{field['id']}/bookings", json=booking_payload)
    assert res.status_code == 200

    overlapping_payload = {
        "start_time": "2024-02-01T10:30:00Z",
        "end_time": "2024-02-01T11:30:00Z",
        "provider": "stripe",
    }
    res = client.post(f"/fields/{field['id']}/bookings", json=overlapping_payload)
    assert res.status_code == 400

