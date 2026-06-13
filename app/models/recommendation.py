from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)

    recommended_category = Column(String(80), nullable=False)
    recommended_difficulty = Column(String(40), nullable=False)
    reason = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())