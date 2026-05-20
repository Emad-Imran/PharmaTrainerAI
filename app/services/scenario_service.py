from app.repositories.scenario_repository import ScenarioRepository


class ScenarioService:
    def __init__(self, scenario_repository: ScenarioRepository):
        self.scenario_repository = scenario_repository

    def get_all_scenarios(self):
        return self.scenario_repository.find_all()

    def get_scenario_by_id(self, scenario_id: int):
        return self.scenario_repository.find_by_id(scenario_id)

    def seed_default_scenarios(self):
        if self.scenario_repository.count_scenarios() > 0:
            return

        scenario_list = [
            {
                "title": "Tablet Coating Humidity Deviation",
                "category": "Process Control",
                "difficulty": "Intermediate",
                "description": "A tablet coating process is showing abnormal humidity, unstable coating thickness, and increasing defect rate.",
                "process_parameters": "Temperature: 28°C | Humidity: 68% | Defect Rate: 6.5% | Machine Status: Warning | Pressure: Stable",
                "question": "What should the operator check first?",
                "option_a": "Continue production without any change",
                "option_b": "Check inlet air humidity and coating parameters",
                "option_c": "Increase conveyor speed immediately",
                "option_d": "Ignore the warning because the machine is still running",
                "correct_option": "B",
                "explanation": "High humidity and coating variation usually indicate that inlet air humidity and coating parameters should be checked first.",
                "reward_points": 120,
            },
            {
                "title": "Packaging Line Defect Detection",
                "category": "Quality Control",
                "difficulty": "Beginner",
                "description": "The packaging inspection system reports an increase in rejected blister packs during the last production cycle.",
                "process_parameters": "Rejected Units: 7.2% | Camera Status: Warning | Conveyor Speed: 1.8 m/s | Seal Quality: Variable",
                "question": "What is the most suitable first action?",
                "option_a": "Inspect camera alignment and packaging seal quality",
                "option_b": "Delete the inspection records",
                "option_c": "Increase speed to finish production earlier",
                "option_d": "Disable the inspection system",
                "correct_option": "A",
                "explanation": "A sudden increase in rejected packs should be investigated by checking inspection alignment and sealing conditions.",
                "reward_points": 100,
            },
            {
                "title": "Machine Vibration Warning",
                "category": "Predictive Maintenance",
                "difficulty": "Advanced",
                "description": "A filling machine shows a continuous increase in vibration level during operation.",
                "process_parameters": "Vibration: High | Motor Load: 82% | Temperature: 41°C | Maintenance Status: Due Soon",
                "question": "What should be done first?",
                "option_a": "Schedule immediate inspection before continuing long production",
                "option_b": "Ignore the vibration until the machine stops",
                "option_c": "Increase motor speed",
                "option_d": "Restart the dashboard only",
                "correct_option": "A",
                "explanation": "Increasing vibration can indicate mechanical wear or imbalance, so inspection should be prioritized.",
                "reward_points": 150,
            },
            {
                "title": "Bioreactor Temperature Drift",
                "category": "Process Control",
                "difficulty": "Intermediate",
                "description": "A bioreactor temperature is slowly drifting above the expected operating range.",
                "process_parameters": "Temperature: 39.2°C | pH: 7.1 | Agitation: Normal | Dissolved Oxygen: Slightly Low",
                "question": "Which response is most appropriate?",
                "option_a": "Check cooling control loop and temperature sensor reliability",
                "option_b": "Increase batch size",
                "option_c": "Ignore because pH is normal",
                "option_d": "Stop all monitoring",
                "correct_option": "A",
                "explanation": "Temperature drift can affect product quality, so control loop and sensor reliability should be checked.",
                "reward_points": 120,
            },
            {
                "title": "Contamination Risk Alert",
                "category": "Safety and Compliance",
                "difficulty": "Advanced",
                "description": "An operator reports that a sterile area door was opened during a sensitive production step.",
                "process_parameters": "Sterile Zone: Alert | Door Event: Unauthorized Opening | Airflow: Stable | Batch Status: Under Review",
                "question": "What is the safest first action?",
                "option_a": "Document the event and follow contamination risk procedure",
                "option_b": "Continue production without documentation",
                "option_c": "Ask the next shift to decide",
                "option_d": "Remove the alert from the system",
                "correct_option": "A",
                "explanation": "Sterile area deviations must be documented and handled according to contamination risk procedures.",
                "reward_points": 150,
            },
            {
                "title": "Pressure Drop in Filling Line",
                "category": "Process Control",
                "difficulty": "Beginner",
                "description": "A liquid filling line shows a sudden pressure drop while filling vials.",
                "process_parameters": "Line Pressure: Low | Fill Volume: Inconsistent | Pump Status: Running | Valve Status: Unknown",
                "question": "What should be checked first?",
                "option_a": "Pump, valve position, and possible leakage",
                "option_b": "Label printer color",
                "option_c": "Operator attendance sheet",
                "option_d": "Office network speed",
                "correct_option": "A",
                "explanation": "Pressure drop with inconsistent fill volume suggests pump, valve, or leakage issues.",
                "reward_points": 100,
            },
        ]

        for item in scenario_list:
            self.scenario_repository.create_scenario(**item)