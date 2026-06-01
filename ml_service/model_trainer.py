import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


class DifficultyLevelModel:
    """
    Machine Learning Classification Model

    This model predicts the next suitable training level:
    Beginner, Intermediate, or Advanced.

    Features used:
    - average_score
    - correct_rate
    - total_attempts
    - current_streak
    - latest_score
    - difficulty_number
    """

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=80,
            random_state=42,
            max_depth=5
        )
        self.label_encoder = LabelEncoder()
        self.is_trained = False

    def _build_training_data(self):
        training_rows = [
            # average_score, correct_rate, total_attempts, current_streak, latest_score, difficulty_number, next_level

            # Beginner recommendation cases
            [20, 0.10, 1, 0, 20, 1, "Beginner"],
            [35, 0.20, 2, 0, 30, 1, "Beginner"],
            [45, 0.30, 3, 1, 40, 1, "Beginner"],
            [55, 0.40, 3, 1, 50, 1, "Beginner"],
            [60, 0.45, 4, 1, 55, 1, "Beginner"],

            # Intermediate recommendation cases
            [70, 0.65, 3, 2, 75, 1, "Intermediate"],
            [72, 0.70, 4, 2, 70, 1, "Intermediate"],
            [75, 0.72, 5, 3, 78, 1, "Intermediate"],
            [68, 0.62, 5, 2, 70, 2, "Intermediate"],
            [74, 0.70, 6, 3, 76, 2, "Intermediate"],
            [78, 0.76, 6, 3, 80, 2, "Intermediate"],

            # Advanced recommendation cases
            [82, 0.80, 6, 4, 85, 2, "Advanced"],
            [85, 0.84, 7, 4, 88, 2, "Advanced"],
            [88, 0.88, 8, 5, 90, 2, "Advanced"],
            [90, 0.90, 8, 5, 92, 3, "Advanced"],
            [86, 0.86, 9, 4, 84, 3, "Advanced"],

            # Cases where advanced users should remain advanced
            [60, 0.55, 8, 1, 55, 3, "Intermediate"],
            [50, 0.45, 6, 0, 45, 2, "Beginner"],
            [65, 0.60, 7, 2, 62, 3, "Intermediate"],
        ]

        columns = [
            "average_score",
            "correct_rate",
            "total_attempts",
            "current_streak",
            "latest_score",
            "difficulty_number",
            "next_level",
        ]

        return pd.DataFrame(training_rows, columns=columns)

    def train(self):
        dataset = self._build_training_data()

        feature_columns = [
            "average_score",
            "correct_rate",
            "total_attempts",
            "current_streak",
            "latest_score",
            "difficulty_number",
        ]

        x_values = dataset[feature_columns]
        y_values = self.label_encoder.fit_transform(dataset["next_level"])

        self.model.fit(x_values, y_values)
        self.is_trained = True

    def predict_level(
        self,
        average_score: float,
        correct_rate: float,
        total_attempts: int,
        current_streak: int,
        latest_score: float,
        difficulty_number: int,
    ):
        if not self.is_trained:
            self.train()

        input_data = np.array([
            [
                average_score,
                correct_rate,
                total_attempts,
                current_streak,
                latest_score,
                difficulty_number,
            ]
        ])

        predicted_class = self.model.predict(input_data)[0]
        predicted_level = self.label_encoder.inverse_transform([predicted_class])[0]

        probabilities = self.model.predict_proba(input_data)[0]
        confidence = float(max(probabilities))

        return {
            "recommended_level": predicted_level,
            "confidence": round(confidence, 2),
        }


difficulty_model = DifficultyLevelModel()
difficulty_model.train()