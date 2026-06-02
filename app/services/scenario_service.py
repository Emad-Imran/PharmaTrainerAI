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

        paper_gamification_manufacturing = (
            "Ulmer et al. — Usage of Digital Twins for Gamification Applications in Manufacturing"
        )

        paper_adaptive_training = (
            "Bucchiarone et al. — Gamification and Virtual Reality for Digital Twin Learning and Training"
        )

        paper_biopharma = (
            "Shahab, Destro & Braatz — Digital Twins in Biopharmaceutical Manufacturing"
        )

        scenario_list = [
            {
                "title": "Packaging Line Defect Detection",
                "category": "Quality Control",
                "difficulty": "Beginner",
                "description": "A packaging inspection screen reports an increase in rejected blister packs during a short production cycle.",
                "process_parameters": "Rejected Units: 7.2% | Camera Status: Warning | Conveyor Speed: 1.8 m/s | Seal Quality: Variable",
                "question": "What should the trainee check first?",
                "option_a": "Inspect camera alignment and packaging seal quality",
                "option_b": "Disable the inspection system",
                "option_c": "Increase conveyor speed",
                "option_d": "Delete the warning record",
                "correct_option": "A",
                "explanation": "The first step is to verify inspection alignment and seal quality because both directly affect packaging rejection.",
                "reward_points": 100,
                "weak_area": "Quality inspection basics",
                "level_order": 1,
                "research_reference": paper_gamification_manufacturing,
                "learning_hint": "Review how feedback, skill levels, and performance indicators support manufacturing training.",
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
                "explanation": "A pressure drop with inconsistent fill volume indicates a possible pump, valve, or leakage issue.",
                "reward_points": 100,
                "weak_area": "Basic process parameter control",
                "level_order": 1,
                "research_reference": paper_biopharma,
                "learning_hint": "Review how process deviations and operator decisions affect biopharmaceutical manufacturing stability.",
            },
            {
                "title": "Basic Safety Alert",
                "category": "Safety and Compliance",
                "difficulty": "Beginner",
                "description": "A safety alert appears during a routine production step.",
                "process_parameters": "Safety Alert: Active | Operator Status: Available | Batch Status: Running | Risk Level: Low",
                "question": "What is the best first response?",
                "option_a": "Acknowledge the alert and follow the safety procedure",
                "option_b": "Ignore the alert because the batch is running",
                "option_c": "Close the system window",
                "option_d": "Ask the next shift to check it",
                "correct_option": "A",
                "explanation": "Even low-risk alerts must be acknowledged and handled using the defined safety procedure.",
                "reward_points": 100,
                "weak_area": "Safety response procedure",
                "level_order": 1,
                "research_reference": paper_adaptive_training,
                "learning_hint": "Review how adaptive training systems guide learners when they make unsafe or weak decisions.",
            },
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
                "explanation": "High humidity and coating variation indicate that inlet air humidity and coating parameters should be checked first.",
                "reward_points": 120,
                "weak_area": "Humidity and coating process control",
                "level_order": 2,
                "research_reference": paper_biopharma,
                "learning_hint": "Review how process monitoring supports deviation response in pharmaceutical manufacturing.",
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
                "weak_area": "Bioprocess control loop monitoring",
                "level_order": 2,
                "research_reference": paper_biopharma,
                "learning_hint": "Review the role of monitoring, abnormality handling, and human-machine collaboration in biopharmaceutical systems.",
            },
            {
                "title": "Quality Trend Deviation",
                "category": "Quality Control",
                "difficulty": "Intermediate",
                "description": "A quality dashboard shows a gradual rise in minor defects over three production cycles.",
                "process_parameters": "Minor Defects: Increasing | Batch Trend: Unstable | Inspection Status: Active | Risk Level: Medium",
                "question": "What is the most suitable action?",
                "option_a": "Analyze the defect trend and check process conditions",
                "option_b": "Ignore minor defects",
                "option_c": "Only update the dashboard color",
                "option_d": "Skip quality review",
                "correct_option": "A",
                "explanation": "A rising defect trend should be analyzed early before it becomes a major quality deviation.",
                "reward_points": 120,
                "weak_area": "Quality trend analysis",
                "level_order": 2,
                "research_reference": paper_gamification_manufacturing,
                "learning_hint": "Review how KPIs and feedback can help learners improve manufacturing decision-making.",
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
                "weak_area": "Predictive maintenance decision-making",
                "level_order": 3,
                "research_reference": paper_adaptive_training,
                "learning_hint": "Review how adaptive training can support complex decisions in simulated production environments.",
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
                "weak_area": "Contamination risk and compliance handling",
                "level_order": 3,
                "research_reference": paper_biopharma,
                "learning_hint": "Review how abnormal events and operator decisions influence biopharmaceutical manufacturing quality.",
            },
            {
                "title": "Multi-Parameter Batch Instability",
                "category": "Process Control",
                "difficulty": "Advanced",
                "description": "A batch shows simultaneous variation in temperature, dissolved oxygen, and defect trend indicators.",
                "process_parameters": "Temperature: High | Dissolved Oxygen: Low | Defect Trend: Rising | Batch Status: Critical",
                "question": "What is the best decision?",
                "option_a": "Investigate combined process deviation before continuing",
                "option_b": "Only check the packaging line",
                "option_c": "Ignore because one parameter is still acceptable",
                "option_d": "Increase production speed",
                "correct_option": "A",
                "explanation": "Multiple unstable parameters indicate a combined deviation that must be investigated before continuing.",
                "reward_points": 150,
                "weak_area": "Multi-parameter deviation analysis",
                "level_order": 3,
                "research_reference": paper_biopharma,
                "learning_hint": "Review how digitalized manufacturing systems support monitoring and abnormality response.",
            },
        ]

        for item in scenario_list:
            self.scenario_repository.create_scenario(**item)