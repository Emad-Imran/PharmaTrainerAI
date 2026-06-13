from sqlalchemy.orm import Session

from app.models.attempt import Attempt


class AttemptRepository:
    def __init__(self, database: Session):
        self.database = database

    def create_attempt(
        self,
        user_id: int,
        scenario_id: int,
        selected_option: str,
        correct_option: str,
        is_correct: bool,
        score: int,
        points_earned: int,
    ):
        attempt = Attempt(
            user_id=user_id,
            scenario_id=scenario_id,
            selected_option=selected_option,
            correct_option=correct_option,
            is_correct=is_correct,
            score=score,
            points_earned=points_earned,
        )

        self.database.add(attempt)
        self.database.commit()
        self.database.refresh(attempt)

        return attempt

    def find_by_id(self, attempt_id: int):
        return self.database.query(Attempt).filter(Attempt.id == attempt_id).first()

    def find_by_user(self, user_id: int):
        return (
            self.database.query(Attempt)
            .filter(Attempt.user_id == user_id)
            .order_by(Attempt.id.desc())
            .all()
        )

    def count_correct_attempts_by_user_and_category(
        self,
        user_id: int,
        scenario_ids: list[int],
    ):
        if not scenario_ids:
            return 0

        return (
            self.database.query(Attempt)
            .filter(
                Attempt.user_id == user_id,
                Attempt.scenario_id.in_(scenario_ids),
                Attempt.is_correct == True,
            )
            .count()
        )

    def calculate_user_performance_summary(self, user_id: int):
        attempts = self.find_by_user(user_id=user_id)

        if not attempts:
            return {
                "average_score": 0,
                "correct_rate": 0,
                "total_attempts": 0,
                "latest_score": 0,
                "latest_difficulty": "Beginner",
            }

        total_attempts = len(attempts)
        total_score = sum(attempt.score for attempt in attempts)
        correct_attempts = sum(1 for attempt in attempts if attempt.is_correct)

        latest_attempt = attempts[0]

        average_score = int(total_score / total_attempts)
        correct_rate = round(correct_attempts / total_attempts, 2)

        return {
            "average_score": average_score,
            "correct_rate": correct_rate,
            "total_attempts": total_attempts,
            "latest_score": latest_attempt.score,
            "latest_difficulty": "Beginner",
        }