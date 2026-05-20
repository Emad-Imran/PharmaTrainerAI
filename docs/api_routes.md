# API and UI Routes

## Main UI Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Home page |
| `/register` | GET | Register form |
| `/register` | POST | Create user |
| `/login` | GET | Login form |
| `/login` | POST | Authenticate user |
| `/dashboard/{user_id}` | GET | User dashboard |
| `/scenarios` | GET | Scenario list |
| `/scenarios/{scenario_id}` | GET | Scenario detail |
| `/scenarios/{scenario_id}/attempt` | POST | Submit answer |
| `/attempts/{attempt_id}/result` | GET | Attempt result |
| `/profile/{user_id}` | GET | User profile |
| `/leaderboard` | GET | Leaderboard |
| `/recommendation/{user_id}` | GET | AI recommendation |
| `/health` | GET | Health check |

## Swagger Documentation

FastAPI automatically provides interactive API documentation at:

`/docs`