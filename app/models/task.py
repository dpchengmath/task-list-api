from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

    def task_dictionary(self):
        return dict(id=self.id, title=self.title, description=self.description, 
                    is_complete = self.is_complete)