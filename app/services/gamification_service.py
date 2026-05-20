from app.patterns.gamification_observer import (
    BadgeObserver,
    PointsObserver,
    SkillScoreObserver,
    StreakObserver,
)
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.skill_score_repository import SkillScoreRepository
from app.repositories.user_repository import UserRepository


class GamificationService:
    def __init__(
        self,
        user_repository: UserRepository,
        scenario_repository: ScenarioRepository,
        attempt_repository: AttemptRepository,
        badge_repository: BadgeRepository,
        skill_score_repository: SkillScoreRepository,
    ):
        self.user_repository = user_repository
        self.scenario_repository = scenario_repository
        self.attempt_repository = attempt_repository
        self.badge_repository = badge_repository
        self.skill_score_repository = skill_score_repository

    def seed_default_badges(self):
        if self.badge_repository.count_badges() > 0:
            return

        badge_list = [
            {
                "name": "Quality Guardian",
                "description": "Earned by completing 2 Quality Control scenarios correctly.",
                "category": "Quality Control",
                "required_correct_attempts": 2,
            },
            {
                "name": "Process Control Starter",
                "description": "Earned by completing 2 Process Control scenarios correctly.",
                "category": "Process Control",
                "required_correct_attempts": 2,
            },
            {
                "name": "Maintenance Hero",
                "description": "Earned by completing 1 Predictive Maintenance scenario correctly.",
                "category": "Predictive Maintenance",
                "required_correct_attempts": 1,
            },
            {
                "name": "Safety First",
                "description": "Earned by completing 1 Safety and Compliance scenario correctly.",
                "category": "Safety and Compliance",
                "required_correct_attempts": 1,
            },
            {
                "name": "Packaging Specialist",
                "description": "Earned by completing 1 Packaging Inspection scenario correctly.",
                "category": "Packaging Inspection",
                "required_correct_attempts": 1,
            },
        ]

        for badge_data in badge_list:
            self.badge_repository.create_badge(**badge_data)

    def apply_gamification_after_attempt(
        self,
        user_id: int,
        scenario_category: str,
        score: int,
        points_earned: int,
        is_correct: bool,
    ):
        observers = [
            PointsObserver(self.user_repository),
            StreakObserver(self.user_repository),
            SkillScoreObserver(self.skill_score_repository),
            BadgeObserver(self),
        ]

        for observer in observers:
            observer.update(
                user_id=user_id,
                scenario_category=scenario_category,
                score=score,
                points_earned=points_earned,
                is_correct=is_correct,
            )

    def evaluate_badges(self, user_id: int):
        all_badges = self.badge_repository.find_all_badges()

        for badge in all_badges:
            scenario_ids = self.scenario_repository.find_ids_by_category(
                category=badge.category,
            )

            correct_attempts = (
                self.attempt_repository.count_correct_attempts_by_user_and_category(
                    user_id=user_id,
                    scenario_ids=scenario_ids,
                )
            )

            if correct_attempts >= badge.required_correct_attempts:
                self.badge_repository.award_badge(
                    user_id=user_id,
                    badge_id=badge.id,
                )