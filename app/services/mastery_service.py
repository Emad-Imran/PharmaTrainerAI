class MasteryService:
    """
    Mastery-based learning logic.

    Progression rule:
    Beginner must be mastered before Intermediate.
    Intermediate must be mastered before Advanced.
    Advanced must be mastered before Industry Exposure.
    """

    def __init__(self, attempt_repository, scenario_repository):
        self.attempt_repository = attempt_repository
        self.scenario_repository = scenario_repository

    def get_mastery_status(self, user_id: int):
        attempts = self.attempt_repository.find_by_user(user_id=user_id)

        level_data = {
            "Beginner": {"total": 0, "correct": 0, "score_sum": 0},
            "Intermediate": {"total": 0, "correct": 0, "score_sum": 0},
            "Advanced": {"total": 0, "correct": 0, "score_sum": 0},
        }

        for attempt in attempts:
            scenario = self.scenario_repository.find_by_id(attempt.scenario_id)

            if not scenario:
                continue

            difficulty = scenario.difficulty

            if difficulty not in level_data:
                continue

            level_data[difficulty]["total"] += 1
            level_data[difficulty]["score_sum"] += attempt.score

            if attempt.is_correct:
                level_data[difficulty]["correct"] += 1

        beginner_mastered = self._is_level_mastered(level_data["Beginner"], 70, 3)
        intermediate_mastered = self._is_level_mastered(level_data["Intermediate"], 75, 3)
        advanced_mastered = self._is_level_mastered(level_data["Advanced"], 80, 3)

        if not beginner_mastered:
            current_level = "Beginner"
            unlocked_level_order = 1
            next_action = "Continue Beginner-level scenarios. Intermediate is locked until Beginner mastery is achieved."
            industry_unlocked = False

        elif not intermediate_mastered:
            current_level = "Intermediate"
            unlocked_level_order = 2
            next_action = "Beginner mastered. Intermediate level is now unlocked. Advanced is still locked."
            industry_unlocked = False

        elif not advanced_mastered:
            current_level = "Advanced"
            unlocked_level_order = 3
            next_action = "Intermediate mastered. Advanced level is now unlocked. Complete Advanced scenarios to unlock industry exposure."
            industry_unlocked = False

        else:
            current_level = "Industry Exposure"
            unlocked_level_order = 4
            next_action = (
                "Advanced level mastered. Industry exposure is now unlocked. "
                "You are ready to focus on specific pharmaceutical manufacturing departments."
            )
            industry_unlocked = True

        return {
            "current_level": current_level,
            "unlocked_level_order": unlocked_level_order,
            "industry_unlocked": industry_unlocked,
            "next_action": next_action,
            "mastery_message": self._build_mastery_message(level_data),
            "beginner_progress": f"{level_data['Beginner']['correct']} / 3",
            "intermediate_progress": f"{level_data['Intermediate']['correct']} / 3",
            "advanced_progress": f"{level_data['Advanced']['correct']} / 3",
            "beginner_mastered": beginner_mastered,
            "intermediate_mastered": intermediate_mastered,
            "advanced_mastered": advanced_mastered,
        }

    def can_access_scenario(self, user_id: int, scenario):
        mastery_status = self.get_mastery_status(user_id=user_id)

        if mastery_status["industry_unlocked"]:
            return True

        return scenario.level_order == mastery_status["unlocked_level_order"]

    def get_locked_message(self, user_id: int, scenario):
        mastery_status = self.get_mastery_status(user_id=user_id)

        return (
            f"{scenario.difficulty} level is locked. "
            f"Current unlocked level is {mastery_status['current_level']}. "
            f"{mastery_status['next_action']}"
        )

    def _is_level_mastered(self, level_record: dict, required_average: int, required_correct: int):
        if level_record["total"] == 0:
            return False

        average_score = int(level_record["score_sum"] / level_record["total"])

        return (
            level_record["correct"] >= required_correct
            and average_score >= required_average
        )

    def _build_mastery_message(self, level_data: dict):
        beginner_average = self._average(level_data["Beginner"])
        intermediate_average = self._average(level_data["Intermediate"])
        advanced_average = self._average(level_data["Advanced"])

        return (
            f"Beginner average: {beginner_average}%, "
            f"Intermediate average: {intermediate_average}%, "
            f"Advanced average: {advanced_average}%."
        )

    def _average(self, level_record: dict):
        if level_record["total"] == 0:
            return 0

        return int(level_record["score_sum"] / level_record["total"])