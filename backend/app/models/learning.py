from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

JSONVariant = JSON().with_variant(JSONB, "postgresql")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(260), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(32), default="beginner", nullable=False)
    icon_name: Mapped[str] = mapped_column(String(48), default="Code2", nullable=False)
    accent_color: Mapped[str] = mapped_column(String(32), default="indigo", nullable=False)
    estimated_hours: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    modules: Mapped[list["Module"]] = relationship(
        back_populates="path", order_by="Module.order_index", cascade="all, delete-orphan"
    )


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path_id: Mapped[int] = mapped_column(ForeignKey("learning_paths.id", ondelete="CASCADE"), index=True)
    slug: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=45, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (UniqueConstraint("path_id", "slug", name="uq_module_path_slug"),)

    path: Mapped["LearningPath"] = relationship(back_populates="modules")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module", order_by="Lesson.order_index", cascade="all, delete-orphan"
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    slug: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    learning_objectives: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    content_blocks: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    key_terms: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    common_mistakes: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    interactive_lab_type: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    starter_code: Mapped[str] = mapped_column(Text, default="", nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (UniqueConstraint("module_id", "slug", name="uq_lesson_module_slug"),)

    module: Mapped["Module"] = relationship(back_populates="lessons")
    quiz: Mapped["Quiz"] = relationship(back_populates="lesson", uselist=False, cascade="all, delete-orphan")


class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(24), default="not_started", nullable=False)  # not_started | in_progress | completed
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    xp_awarded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),)


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int | None] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True, index=True)
    module_id: Mapped[int | None] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    topic: Mapped[str] = mapped_column(String(120), default="General AI", nullable=False)
    difficulty: Mapped[str] = mapped_column(String(32), default="medium", nullable=False)
    pass_percentage: Mapped[int] = mapped_column(Integer, default=70, nullable=False)
    time_limit_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0 = untimed
    xp_reward: Mapped[int] = mapped_column(Integer, default=30, nullable=False)

    lesson: Mapped["Lesson"] = relationship(back_populates="quiz")
    questions: Mapped[list["Question"]] = relationship(
        back_populates="quiz", order_by="Question.order_index", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), index=True)
    question_type: Mapped[str] = mapped_column(String(32), default="multiple_choice", nullable=False)
    # multiple_choice | multiple_select | true_false | predict_output | fill_blank | code_completion | debugging | short_answer
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    code_snippet: Mapped[str] = mapped_column(Text, default="", nullable=False)
    options: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    correct_answer: Mapped[dict] = mapped_column(JSONVariant, default=dict, nullable=False)  # {"value": ...}
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    topic_tag: Mapped[str] = mapped_column(String(80), default="Foundations", nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    quiz: Mapped["Quiz"] = relationship(back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), index=True)
    answers: Mapped[dict] = mapped_column(JSONVariant, default=dict, nullable=False)
    score_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_count: Mapped[int] = mapped_column(Integer, nullable=False)
    topic_breakdown: Mapped[dict] = mapped_column(JSONVariant, default=dict, nullable=False)
    xp_awarded: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class CodingChallenge(Base):
    __tablename__ = "coding_challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    path_slug: Mapped[str] = mapped_column(String(80), default="python-foundations", index=True, nullable=False)
    mode: Mapped[str] = mapped_column(String(32), default="write_run", nullable=False)
    # write_run | complete_code | debug_code | predict_output | challenge
    difficulty: Mapped[str] = mapped_column(String(24), default="easy", nullable=False)
    starter_code: Mapped[str] = mapped_column(Text, nullable=False)
    solution_code: Mapped[str] = mapped_column(Text, nullable=False)
    hints: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    test_cases: Mapped[list] = mapped_column(JSONVariant, default=list, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, default="", nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=40, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class CodeSubmission(Base):
    __tablename__ = "code_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("coding_challenges.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    passed_tests: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tests: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    used_hint: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    xp_awarded: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    execution_time_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    feedback: Mapped[dict] = mapped_column(JSONVariant, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class ExecutionResult(Base):
    __tablename__ = "execution_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    stdin: Mapped[str] = mapped_column(Text, default="", nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    stdout: Mapped[str] = mapped_column(Text, default="", nullable=False)
    stderr: Mapped[str] = mapped_column(Text, default="", nullable=False)
    execution_time_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sandbox_mode: Mapped[str] = mapped_column(String(24), default="subprocess", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class SavedSnippet(Base):
    __tablename__ = "saved_snippets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
