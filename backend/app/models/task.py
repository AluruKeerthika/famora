
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from backend.app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    assigned_to = Column(String(100), nullable=True)

    due_date = Column(DateTime, nullable=True)

    status = Column(
        String(20),
        default="pending",
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
