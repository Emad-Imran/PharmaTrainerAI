from app.patterns.ai_recommendation_adapter import RecommendationEngineAdapter
from app.patterns.ml_service_adapter import MLServiceAdapter
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.skill_score_repository import SkillScoreRepository
from app.repositories.user_repository import UserRepository


class RuleBasedRecommendationService(RecommendationEngineAdapter):
    def __init__(
        self,
        skill_score_repository: SkillScoreRepository,
        scenario_repository: ScenarioRepository,
        recommendation_repository: RecommendationRepository,
        attempt_repository: AttemptRepository | None = None,
        user_repository: UserRepository | None = None,
        ml_service_adapter: MLServiceAdapter | None = None,
    ):
        self.skill_score_repository = skill_score_repository
        self.scenario_repository = scenario_repository
        self.recommendation_repository = recommendation_repository
        self.attempt_repository = attempt_repository
        self.user_repository = user_repository
        self.ml_service_adapter = ml_service_adapter or MLServiceAdapter()

    def recommend_next_scenario(self, user_id: int):
        ml_prediction = self._get_ml_prediction(user_id=user_id)

        skill_scores = self.skill_score_repository.find_by_user(user_id=user_id)

        if not skill_scores:
            scenario = self.scenario_repository.find_by_category_and_difficulty(
                category="Process Control",
                difficulty=ml_prediction.get("recommended_level") or "Beginner",
            )

            if not scenario:
                scenario = self.scenario_repository.find_first_available()

            if not scenario:
                return None

            return self.recommendation_repository.create_recommendation(
                user_id=user_id,
                scenario_id=scenario.id,
                recommended_category=scenario.category,
                recommended_difficulty=scenario.difficulty,
                reason=(
                    f"ML model recommended {scenario.difficulty} level with "
                    f"{ml_prediction.get('confidence', 0)} confidence. "
                    f"{ml_prediction.get('explanation')}"
                ),
            )

        weakest_skill = min(skill_scores, key=lambda item: item.average_score)

        ml_recommended_level = ml_prediction.get("recommended_level")

        if ml_recommended_level:
            recommended_difficulty = ml_recommended_level
        else:
            recommended_difficulty = self._fallback_difficulty(
                average_score=weakest_skill.average_score
            )

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
            f"ML-assisted recommendation selected {scenario.difficulty} level. "
            f"Your weakest area is {weakest_skill.category} with an average score "
            f"of {weakest_skill.average_score}%. "
            f"Model confidence: {ml_prediction.get('confidence', 0)}. "
            f"{ml_prediction.get('explanation')}"
        )

        return self.recommendation_repository.create_recommendation(
            user_id=user_id,
            scenario_id=scenario.id,
            recommended_category=scenario.category,
            recommended_difficulty=scenario.difficulty,
            reason=reason,
        )

    def _get_ml_prediction(self, user_id: int):
        if not self.attempt_repository or not self.user_repository:
            return {
                "recommended_level": "Beginner",
                "confidence": 0.0,
                "model_type": "Rule-based fallback",
                "explanation": "Performance data was incomplete, so the system used fallback logic.",
            }

        user = self.user_repository.find_by_id(user_id=user_id)

        if not user:
            return {
                "recommended_level": "Beginner",
                "confidence": 0.0,
                "model_type": "Rule-based fallback",
                "explanation": "User was not found, so fallback recommendation was used.",
            }

        performance = self.attempt_repository.calculate_user_performance_summary(
            user_id=user_id
        )

        return self.ml_service_adapter.predict_next_level(
            average_score=performance["average_score"],
            correct_rate=performance["correct_rate"],
            total_attempts=performance["total_attempts"],
            current_streak=user.current_streak,
            latest_score=performance["latest_score"],
            current_difficulty=performance["latest_difficulty"],
        )

    def _fallback_difficulty(self, average_score: int):
        if average_score < 50:
            return "Beginner"

        if average_score < 75:
            return "Intermediate"

        return "Advanced"