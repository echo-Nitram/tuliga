from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..models import SessionLocal, Base, engine
from ..models.conversations import Conversation
from ..models.messages import Message

router = APIRouter()

# Create tables when router is imported
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ConversationCreate(BaseModel):
    title: str | None = None


@router.post("/conversations")
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    convo = Conversation(title=conversation.title)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return {"id": convo.id, "title": convo.title}


class MessageCreate(BaseModel):
    sender: str
    content: str


@router.post("/conversations/{conversation_id}/messages")
def create_message(conversation_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    convo = db.get(Conversation, conversation_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = Message(conversation_id=conversation_id, sender=message.sender, content=message.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "sender": msg.sender,
        "content": msg.content,
        "timestamp": msg.timestamp.isoformat(),
    }


@router.get("/conversations/{conversation_id}/messages")
def read_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp)
        .all()
    )
    return [
        {
            "id": m.id,
            "sender": m.sender,
            "content": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in messages
    ]
