"""Модели базы данных."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utc_now() -> datetime:
    """Возвращает текущее время в UTC."""
    return datetime.now(timezone.utc)


class Task(db.Model):
    """Задача в списке дел."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    def __repr__(self) -> str:
        return f"<Task {self.id}: {self.title!r}>"
