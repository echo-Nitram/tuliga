from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routes.messages import router
from backend.models import Base, engine

app = FastAPI()
app.include_router(router)


def setup_module(module):
    # Reset database for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


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
