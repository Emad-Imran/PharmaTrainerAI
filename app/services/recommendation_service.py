from app.patterns.ai_recommendation_adapter import RecommendationEngineAdapter
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.skill_score_repository import SkillScoreRepository


class RuleBasedRecommendationService(RecommendationEngineAdapter):
    def __init__(
        self,
        skill_score_repository: SkillScoreRepository,
        scenario_repository: ScenarioRepository,
        recommendation_repository: RecommendationRepository,
    ):
        self.skill_score_repository = skill_score_repository
        self.scenario_repository = scenario_repository
        self.recommendation_repository = recommendation_repository

    def recommend_next_scenario(self, user_id: int):
        skill_scores = self.skill_score_repository.find_by_user(user_id=user_id)

        if not skill_scores:
            scenario = self.scenario_repository.find_first_available()

            if not scenario:
                return None

            return self.recommendation_repository.create_recommendation(
                user_id=user_id,
                scenario_id=scenario.id,
                recommended_category=scenario.category,
                recommended_difficulty=scenario.difficulty,
                reason="You are starting your training journey. The system recommends the first available challenge.",
            )

        weakest_skill = min(skill_scores, key=lambda item: item.average_score)

        if weakest_skill.average_score < 50:
            recommended_difficulty = "Beginner"
        elif weakest_skill.average_score < 75:
            recommended_difficulty = "Intermediate"
        else:
            recommended_difficulty = "Advanced"

        scenario = self.scenario_repository.find_by_category_and_difficulty(
            category=weakest_skill.category,
            difficulty=recommended_difficulty,
        )

        if not scenario:
            scenario = self.scenario_repository.find_first_by_category(
                category=weakest_skill.category,
            )

        if not scenario:
            scenario = self.scenario_repository.find_first_available()

        if not scenario:
            return None

        reason = (
            f"Your weakest area is {weakest_skill.category} with an average score "
            f"of {weakest_skill.average_score}%. The system recommends a "
            f"{scenario.difficulty} challenge to improve this skill."
        )

        return self.recommendation_repository.create_recommendation(
            user_id=user_id,
            scenario_id=scenario.id,
            recommended_category=scenario.category,
            recommended_difficulty=scenario.difficulty,
            reason=reason,
        )