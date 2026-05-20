from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)

    selected_option = Column(String(1), nullable=False)
    correct_option = Column(String(1), nullable=False)

    is_correct = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    points_earned = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())