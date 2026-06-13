from sqlalchemy.orm import Session

from app.models.skill_score import SkillScore


class SkillScoreRepository:
    def __init__(self, database: Session):
        self.database = database

    def find_by_user_and_category(self, user_id: int, category: str):
        return (
            self.database.query(SkillScore)
            .filter(
                SkillScore.user_id == user_id,
                SkillScore.category == category,
            )
            .first()
        )

    def find_by_user(self, user_id: int):
        return (
            self.database.query(SkillScore)
            .filter(SkillScore.user_id == user_id)
            .order_by(SkillScore.category.asc())
            .all()
        )

    def update_skill_score(
        self,
        user_id: int,
        category: str,
        score: int,
        is_correct: bool,
    ):
        skill_score = self.find_by_user_and_category(
            user_id=user_id,
            category=category,
        )

        if not skill_score:
            skill_score = SkillScore(
                user_id=user_id,
                category=category,
                total_attempts=0,
                correct_attempts=0,
                average_score=0,
            )
            self.database.add(skill_score)
            self.database.commit()
            self.database.refresh(skill_score)

        old_total_score = skill_score.average_score * skill_score.total_attempts

        skill_score.total_attempts += 1

        if is_correct:
            skill_score.correct_attempts += 1

        new_average = int((old_total_score + score) / skill_score.total_attempts)
        skill_score.average_score = new_average

        self.database.commit()
        self.database.refresh(skill_score)

        return skill_score