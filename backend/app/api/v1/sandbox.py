from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.learning import ExecutionResult, SavedSnippet
from app.services.sandbox import execute_python_sandbox
from app.services.rate_limit import rate_limiter
from app.core.config import settings
from sqlalchemy import select

router = APIRouter()


class RunIn(BaseModel):
    code: str
    stdin: str = ""


class SaveSnippetIn(BaseModel):
    title: str
    code: str


@router.post("/execute")
def execute_code(
    payload: RunIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not rate_limiter.allow(f"sandbox:{current_user.id}", settings.SANDBOX_RATE_LIMIT_PER_MINUTE):
        raise HTTPException(429, "Rate limit exceeded. Please wait before running more code.")
    if len(payload.code) > 65536:
        raise HTTPException(400, "Code exceeds maximum length of 65536 characters")
    
    result = execute_python_sandbox(payload.code, payload.stdin)
    
    record = ExecutionResult(
        user_id=current_user.id,
        code=payload.code[:4000],
        stdin=payload.stdin[:500],
        success=result.get("success", False),
        stdout=result.get("stdout", "")[:8000],
        stderr=result.get("stderr", "")[:4000],
        execution_time_ms=result.get("execution_time_ms", 0.0),
        sandbox_mode=result.get("sandbox_mode", "subprocess"),
    )
    db.add(record)
    db.commit()
    return {
        "success": result.get("success", False),
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "execution_time_ms": result.get("execution_time_ms", 0.0),
        "sandbox_mode": result.get("sandbox_mode", "subprocess"),
    }


@router.get("/snippets")
def list_snippets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    snippets = db.scalars(
        select(SavedSnippet).where(SavedSnippet.user_id == current_user.id).order_by(SavedSnippet.updated_at.desc()).limit(20)
    ).all()
    return [{"id": s.id, "title": s.title, "code": s.code, "updated_at": s.updated_at.isoformat()} for s in snippets]


@router.post("/snippets")
def save_snippet(payload: SaveSnippetIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    snippet = SavedSnippet(user_id=current_user.id, title=payload.title, code=payload.code)
    db.add(snippet)
    db.commit()
    return {"id": snippet.id, "title": snippet.title}
