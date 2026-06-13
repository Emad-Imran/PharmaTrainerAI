from app.patterns.scoring_strategy import ScoringStrategyFactory
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.skill_score_repository import SkillScoreRepository
from app.repositories.user_repository import UserRepository
from app.services.gamification_service import GamificationService


class AttemptService:
    def __init__(
        self,
        attempt_repository: AttemptRepository,
        scenario_repository: ScenarioRepository,
        user_repository: UserRepository,
        badge_repository: BadgeRepository,
        skill_score_repository: SkillScoreRepository,
    ):
        self.attempt_repository = attempt_repository
        self.scenario_repository = scenario_repository
        self.user_repository = user_repository
        self.badge_repository = badge_repository
        self.skill_score_repository = skill_score_repository

    def submit_answer(self, user_id: int, scenario_id: int, selected_option: str):
        scenario = self.scenario_repository.find_by_id(scenario_id)

        if not scenario:
            return None

        selected_option = selected_option.upper()
        correct_option = scenario.correct_option.upper()

        is_correct = selected_option == correct_option

        scoring_strategy = ScoringStrategyFactory.get_strategy(scenario.difficulty)

        score, points_earned = scoring_strategy.calculate_score(
            is_correct=is_correct,
            reward_points=scenario.reward_points,
        )

        attempt = self.attempt_repository.create_attempt(
            user_id=user_id,
            scenario_id=scenario_id,
            selected_option=selected_option,
            correct_option=correct_option,
            is_correct=is_correct,
            score=score,
            points_earned=points_earned,
        )

        gamification_service = GamificationService(
            user_repository=self.user_repository,
            scenario_repository=self.scenario_repository,
            attempt_repository=self.attempt_repository,
            badge_repository=self.badge_repository,
            skill_score_repository=self.skill_score_repository,
        )

        gamification_service.apply_gamification_after_attempt(
            user_id=user_id,
            scenario_category=scenario.category,
            score=score,
            points_earned=points_earned,
            is_correct=is_correct,
        )

        return attempt