from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_user_timezone
from app.db.session import get_db
from app.models.user import User
from app.models.mentor import AIConversation, AIMessage
from app.models.gamification import UserLevel
from app.services.mentor import generate_mentor_reply
from app.services.gamification import increment_quest_progress, record_qualifying_activity
from app.services.rate_limit import rate_limiter
from app.core.config import settings
import asyncio

router = APIRouter()


class ChatIn(BaseModel):
    conversation_id: int | None = None
    message: str
    mode: str = "hint"
    context: dict = {}


@router.post("/chat")
async def chat_with_mentor(
    payload: ChatIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tz: str = Depends(get_user_timezone),
):
    if not rate_limiter.allow(f"mentor:{current_user.id}", settings.MENTOR_RATE_LIMIT_PER_MINUTE):
        raise HTTPException(429, "AI Mentor rate limit reached. Please wait a moment.")
    if len(payload.message) > 4000:
        raise HTTPException(400, "Message too long (max 4000 chars)")

    # Get or create conversation
    if payload.conversation_id:
        conv = db.scalar(select(AIConversation).where(
            AIConversation.id == payload.conversation_id,
            AIConversation.user_id == current_user.id,
        ))
        if not conv:
            raise HTTPException(404, "Conversation not found")
    else:
        lvl = db.scalar(select(UserLevel).where(UserLevel.user_id == current_user.id))
        ctx_snap = {**payload.context, "level": lvl.current_level if lvl else 1}
        conv = AIConversation(
            user_id=current_user.id,
            title=payload.message[:60] + ("…" if len(payload.message) > 60 else ""),
            mode=payload.mode,
            context_snapshot=ctx_snap,
        )
        db.add(conv)
        db.flush()

    # Build history (last 10 messages)
    history_msgs = db.scalars(
        select(AIMessage).where(AIMessage.conversation_id == conv.id).order_by(AIMessage.created_at.desc()).limit(10)
    ).all()
    history = [{"role": m.role, "content": m.content} for m in reversed(history_msgs)]

    # Enrich context
    lvl = db.scalar(select(UserLevel).where(UserLevel.user_id == current_user.id))
    context = {
        **payload.context,
        "level": lvl.current_level if lvl else 1,
        "experience": "beginner" if (lvl.current_level if lvl else 1) <= 2 else "intermediate",
    }

    reply_data = await generate_mentor_reply(payload.message, payload.mode, context, history)

    # Persist messages
    db.add(AIMessage(conversation_id=conv.id, role="user", content=payload.message))
    db.add(AIMessage(
        conversation_id=conv.id, role="assistant",
        content=reply_data["content"],
        provider_used=reply_data.get("provider_used", "local_socratic_fallback"),
        tokens_used=reply_data.get("tokens_used", 0),
    ))

    increment_quest_progress(db, current_user.id, "mentor_questions", 1, tz)
    record_qualifying_activity(db, current_user.id, tz, mentor_delta=1)
    db.commit()

    return {
        "conversation_id": conv.id,
        "reply": reply_data["content"],
        "provider_used": reply_data.get("provider_used"),
        "mode": payload.mode,
    }


@router.get("/conversations")
def list_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    convs = db.scalars(
        select(AIConversation).where(AIConversation.user_id == current_user.id).order_by(AIConversation.updated_at.desc()).limit(30)
    ).all()
    return [{"id": c.id, "title": c.title, "mode": c.mode, "updated_at": c.updated_at.isoformat()} for c in convs]


@router.get("/conversations/{conv_id}")
def get_conversation(conv_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = db.scalar(select(AIConversation).where(AIConversation.id == conv_id, AIConversation.user_id == current_user.id))
    if not conv:
        raise HTTPException(404, "Conversation not found")
    messages = db.scalars(select(AIMessage).where(AIMessage.conversation_id == conv.id).order_by(AIMessage.created_at)).all()
    return {
        "id": conv.id, "title": conv.title, "mode": conv.mode,
        "messages": [{"id": m.id, "role": m.role, "content": m.content, "created_at": m.created_at.isoformat()} for m in messages],
    }
