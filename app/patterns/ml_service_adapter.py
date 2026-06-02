import os

import requests


class MLServiceAdapter:
    """
    Adapter Pattern:
    Connects the core training service with the ML recommendation service.

    In local development, the ML service runs on 127.0.0.1:9000.
    In Docker Compose, the ML service is reached using the service name:
    http://ml_service:9000
    """

    def __init__(self, service_url: str | None = None):
        self.service_url = service_url or os.getenv(
            "ML_SERVICE_URL",
            "http://127.0.0.1:9000",
        )

    def predict_next_level(
        self,
        average_score: float,
        correct_rate: float,
        total_attempts: int,
        current_streak: int,
        latest_score: float,
        current_difficulty: str,
    ):
        payload = {
            "average_score": average_score,
            "correct_rate": correct_rate,
            "total_attempts": total_attempts,
            "current_streak": current_streak,
            "latest_score": latest_score,
            "current_difficulty": current_difficulty,
        }

        try:
            response = requests.post(
                f"{self.service_url}/predict-level",
                json=payload,
                timeout=3,
            )

            response.raise_for_status()
            return response.json()

        except requests.RequestException:
            return {
                "recommended_level": None,
                "confidence": 0.0,
                "model_type": "Rule-based fallback",
                "explanation": (
                    "ML service is unavailable, so the system used fallback "
                    "recommendation logic."
                ),
            }