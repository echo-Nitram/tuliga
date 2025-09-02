from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routes.messages import router
from . import run_migrations

app = FastAPI()
app.include_router(router)


def setup_module(module):
    # Reset database for tests
    run_migrations()


def test_message_flow():
    client = TestClient(app)
    # Create conversation
    response = client.post("/conversations", json={"title": "General"})
    assert response.status_code == 200
    convo = response.json()
    convo_id = convo["id"]

    # Send messages
    r1 = client.post(
        f"/conversations/{convo_id}/messages",
        json={"sender": "Alice", "content": "Hola"},
    )
    assert r1.status_code == 200
    r2 = client.post(
        f"/conversations/{convo_id}/messages",
        json={"sender": "Bob", "content": "Qué tal"},
    )
    assert r2.status_code == 200

    # Fetch messages
    r3 = client.get(f"/conversations/{convo_id}/messages")
    assert r3.status_code == 200
    messages = r3.json()
    assert len(messages) == 2
    assert messages[0]["content"] == "Hola"
    assert messages[1]["sender"] == "Bob"


def test_list_conversations():
    run_migrations()
    client = TestClient(app)

    r0 = client.get("/conversations")
    assert r0.status_code == 200
    assert r0.json() == []

    c1 = client.post("/conversations", json={"title": "General"})
    assert c1.status_code == 200
    c2 = client.post("/conversations", json={"title": "Random"})
    assert c2.status_code == 200

    r1 = client.get("/conversations")
    assert r1.status_code == 200
    convos = r1.json()
    assert len(convos) == 2
    titles = {c["title"] for c in convos}
    assert {"General", "Random"} <= titles
