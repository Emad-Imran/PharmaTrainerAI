from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation


class RecommendationRepository:
    def __init__(self, database: Session):
        self.database = database

    def create_recommendation(
        self,
        user_id: int,
        scenario_id: int,
        recommended_category: str,
        recommended_difficulty: str,
        reason: str,
    ):
        recommendation = Recommendation(
            user_id=user_id,
            scenario_id=scenario_id,
            recommended_category=recommended_category,
            recommended_difficulty=recommended_difficulty,
            reason=reason,
        )

        self.database.add(recommendation)
        self.database.commit()
        self.database.refresh(recommendation)

        return recommendation

    def find_latest_by_user(self, user_id: int):
        return (
            self.database.query(Recommendation)
            .filter(Recommendation.user_id == user_id)
            .order_by(Recommendation.id.desc())
            .first()
        )