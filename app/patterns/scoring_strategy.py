class ScenarioScoringStrategy:
    def calculate_score(self, is_correct: bool, reward_points: int) -> tuple[int, int]:
        raise NotImplementedError


class StandardScenarioScoring(ScenarioScoringStrategy):
    def calculate_score(self, is_correct: bool, reward_points: int) -> tuple[int, int]:
        if is_correct:
            return 100, reward_points

        return 0, 0


class PracticeScenarioScoring(ScenarioScoringStrategy):
    def calculate_score(self, is_correct: bool, reward_points: int) -> tuple[int, int]:
        if is_correct:
            return 100, reward_points

        return 25, 10


class ScoringStrategyFactory:
    @staticmethod
    def get_strategy(difficulty: str) -> ScenarioScoringStrategy:
        if difficulty.lower() == "beginner":
            return PracticeScenarioScoring()

        return StandardScenarioScoring()