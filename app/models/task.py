from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    def to_dict(self):
            return dict(
                id=self.id,
                title=self.title,
                description=self.description,
                is_complete = bool(self.completed_at)
            )
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"]
        )

        return new_task