from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

JSONVariant = JSON().with_variant(JSONB, "postgresql")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    problem_statement: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(32), default="intermediate", nullable=False)
    technologies: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    prerequisites: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    learning_objectives: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    milestones: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    evaluation_criteria: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    dataset_name: Mapped[str] = mapped_column(String(140), default="", nullable=False)
    sample_dataset: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    starter_code: Mapped[str] = mapped_column(Text, nullable=False)
    required_keywords: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=250, nullable=False)
    badge_code: Mapped[str] = mapped_column(String(80), default="rag_builder", nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    completed_milestones: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    evaluation_report: Mapped[dict] = mapped_column(JSONVariant, default=dict, nullable=False)
    xp_awarded: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
