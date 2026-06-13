from app.core.database import Base, engine

from app.models.attempt import Attempt
from app.models.badge import Badge
from app.models.recommendation import Recommendation
from app.models.scenario import Scenario
from app.models.skill_score import SkillScore
from app.models.user import User
from app.models.user_badge import UserBadge


def create_database_tables():
    Base.metadata.create_all(bind=engine)