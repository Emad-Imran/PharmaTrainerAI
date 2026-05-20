from sqlalchemy.orm import Session

from app.models.scenario import Scenario


class ScenarioRepository:
    def __init__(self, database: Session):
        self.database = database

    def find_all(self):
        return self.database.query(Scenario).order_by(Scenario.id.asc()).all()

    def find_by_id(self, scenario_id: int):
        return self.database.query(Scenario).filter(Scenario.id == scenario_id).first()

    def count_scenarios(self):
        return self.database.query(Scenario).count()

    def create_scenario(
        self,
        title: str,
        category: str,
        difficulty: str,
        description: str,
        process_parameters: str,
        question: str,
        option_a: str,
        option_b: str,
        option_c: str,
        option_d: str,
        correct_option: str,
        explanation: str,
        reward_points: int,
    ):
        scenario = Scenario(
            title=title,
            category=category,
            difficulty=difficulty,
            description=description,
            process_parameters=process_parameters,
            question=question,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
            explanation=explanation,
            reward_points=reward_points,
        )

        self.database.add(scenario)
        self.database.commit()
        self.database.refresh(scenario)

        return scenario
    def find_ids_by_category(self, category: str):
        scenarios = (
            self.database.query(Scenario)
            .filter(Scenario.category == category)
            .all()
        )

        return [scenario.id for scenario in scenarios]
    def find_by_category_and_difficulty(self, category: str, difficulty: str):
        return (
            self.database.query(Scenario)
            .filter(
                Scenario.category == category,
                Scenario.difficulty == difficulty,
            )
            .first()
        )

    def find_first_by_category(self, category: str):
        return (
            self.database.query(Scenario)
            .filter(Scenario.category == category)
            .first()
        )

    def find_first_available(self):
        return self.database.query(Scenario).order_by(Scenario.id.asc()).first()