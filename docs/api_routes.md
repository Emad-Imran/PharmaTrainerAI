# API and UI Routes

## Core Training Service Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Home page |
| `/register` | GET | Register form |
| `/register` | POST | Create user |
| `/login` | GET | Login form |
| `/login` | POST | Authenticate user |
| `/dashboard/{user_id}` | GET | User dashboard |
| `/scenarios` | GET | Adaptive scenario list |
| `/scenarios/{scenario_id}` | GET | Scenario detail if level is unlocked |
| `/scenarios/{scenario_id}/attempt` | POST | Submit scenario answer |
| `/attempts/{attempt_id}/result` | GET | Attempt result and mastery feedback |
| `/profile/{user_id}` | GET | User profile |
| `/leaderboard` | GET | Leaderboard |
| `/recommendation/{user_id}` | GET | ML-assisted recommendation |
| `/industry-exposure/{user_id}` | GET | Industry exposure page after Advanced mastery |
| `/health` | GET | Core app health check |
| `/docs` | GET | Swagger documentation |

---

## ML Recommendation Service Routes

| Route | Method | Purpose |
|---|---|---|
| `/health` | GET | ML service health check |
| `/predict-level` | POST | Predict next suitable training level |
| `/docs` | GET | Swagger documentation for ML service |

---

## ML Prediction Request Example

```json
{
  "average_score": 72,
  "correct_rate": 0.7,
  "total_attempts": 4,
  "current_streak": 2,
  "latest_score": 75,
  "current_difficulty": "Beginner"
}