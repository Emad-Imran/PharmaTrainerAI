from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    total_points = Column(Integer, default=0)
    current_level = Column(String(50), default="Beginner")
    current_streak = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())