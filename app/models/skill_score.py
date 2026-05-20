from sqlalchemy import Column, Integer, String, UniqueConstraint

from app.core.database import Base


class SkillScore(Base):
    __tablename__ = "skill_scores"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    category = Column(String(80), nullable=False)

    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    average_score = Column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("user_id", "category", name="unique_user_category_score"),
    )