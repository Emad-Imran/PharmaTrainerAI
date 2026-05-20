from app.repositories.attempt_repository import AttemptRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.skill_score_repository import SkillScoreRepository
from app.repositories.user_repository import UserRepository
from app.services.attempt_service import AttemptService


class ScenarioSubmissionFacade:
    """
    Facade Pattern:
    This class provides one simplified interface for the complete scenario
    submission workflow.

    Without this facade, the route/controller would need to manually create
    multiple repositories and services every time a user submits an answer.
    """

    def __init__(self, database):
        self.database = database

    def submit_answer(self, user_id: int, scenario_id: int, selected_option: str):
        attempt_repository = AttemptRepository(self.database)
        scenario_repository = ScenarioRepository(self.database)
        user_repository = UserRepository(self.database)
        badge_repository = BadgeRepository(self.database)
        skill_score_repository = SkillScoreRepository(self.database)

        attempt_service = AttemptService(
            attempt_repository=attempt_repository,
            scenario_repository=scenario_repository,
            user_repository=user_repository,
            badge_repository=badge_repository,
            skill_score_repository=skill_score_repository,
        )

        return attempt_service.submit_answer(
            user_id=user_id,
            scenario_id=scenario_id,
            selected_option=selected_option,
        )