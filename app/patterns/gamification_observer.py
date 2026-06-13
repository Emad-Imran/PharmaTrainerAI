class GamificationObserver:
    """
    Observer Pattern:
    Base observer class for actions that should happen after a scenario attempt.
    """

    def update(self, user_id: int, scenario_category: str, score: int, points_earned: int, is_correct: bool):
        raise NotImplementedError


class PointsObserver(GamificationObserver):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def update(self, user_id: int, scenario_category: str, score: int, points_earned: int, is_correct: bool):
        self.user_repository.add_points(user_id=user_id, points=points_earned)


class StreakObserver(GamificationObserver):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def update(self, user_id: int, scenario_category: str, score: int, points_earned: int, is_correct: bool):
        self.user_repository.update_streak(user_id=user_id, is_correct=is_correct)


class SkillScoreObserver(GamificationObserver):
    def __init__(self, skill_score_repository):
        self.skill_score_repository = skill_score_repository

    def update(self, user_id: int, scenario_category: str, score: int, points_earned: int, is_correct: bool):
        self.skill_score_repository.update_skill_score(
            user_id=user_id,
            category=scenario_category,
            score=score,
            is_correct=is_correct,
        )


class BadgeObserver(GamificationObserver):
    def __init__(self, gamification_service):
        self.gamification_service = gamification_service

    def update(self, user_id: int, scenario_category: str, score: int, points_earned: int, is_correct: bool):
        self.gamification_service.evaluate_badges(user_id=user_id)