import requests


class MLServiceAdapter:
    """
    Adapter Pattern:
    This adapter connects the main training application with the external
    ML recommendation microservice.

    If the ML service is unavailable, the main app can still continue by
    using rule-based fallback logic.
    """

    def __init__(self, service_url: str = "http://127.0.0.1:9000"):
        self.service_url = service_url

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
                "explanation": "ML service is unavailable, so the system used fallback recommendation logic.",
            }