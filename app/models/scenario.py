from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(160), nullable=False)
    category = Column(String(80), nullable=False)
    difficulty = Column(String(40), nullable=False)

    description = Column(Text, nullable=False)
    process_parameters = Column(Text, nullable=False)

    question = Column(Text, nullable=False)

    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)

    correct_option = Column(String(1), nullable=False)
    explanation = Column(Text, nullable=False)

    reward_points = Column(Integer, default=100)