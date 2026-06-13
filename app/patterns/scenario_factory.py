class ScenarioCategory:
    def __init__(self, name: str, focus_area: str, display_label: str):
        self.name = name
        self.focus_area = focus_area
        self.display_label = display_label


class ScenarioCategoryFactory:
    """
    Factory Pattern:
    Creates category metadata objects based on the scenario category.

    This keeps category-related display information separate from database
    and UI logic.
    """

    @staticmethod
    def create_category(category_name: str) -> ScenarioCategory:
        normalized_name = category_name.strip().lower()

        if normalized_name == "process control":
            return ScenarioCategory(
                name="Process Control",
                focus_area="Monitoring and stabilizing production parameters",
                display_label="Process Control Challenge",
            )

        if normalized_name == "quality control":
            return ScenarioCategory(
                name="Quality Control",
                focus_area="Detecting product defects and quality risks",
                display_label="Quality Control Challenge",
            )

        if normalized_name == "predictive maintenance":
            return ScenarioCategory(
                name="Predictive Maintenance",
                focus_area="Identifying early equipment failure signals",
                display_label="Maintenance Challenge",
            )

        if normalized_name == "safety and compliance":
            return ScenarioCategory(
                name="Safety and Compliance",
                focus_area="Handling safety risks and compliance deviations",
                display_label="Safety Challenge",
            )

        if normalized_name == "packaging inspection":
            return ScenarioCategory(
                name="Packaging Inspection",
                focus_area="Inspecting packaging defects and line quality",
                display_label="Packaging Challenge",
            )

        return ScenarioCategory(
            name=category_name,
            focus_area="General manufacturing decision-making",
            display_label="Manufacturing Challenge",
        )