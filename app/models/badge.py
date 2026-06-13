from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(80), nullable=False)
    required_correct_attempts = Column(Integer, default=1)