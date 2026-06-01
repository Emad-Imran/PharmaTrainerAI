from pydantic import BaseModel, Field
from fastapi import FastAPI

from model_trainer import difficulty_model


class LevelPredictionRequest(BaseModel):
    average_score: float = Field(ge=0, le=100)
    correct_rate: float = Field(ge=0, le=1)
    total_attempts: int = Field(ge=0)
    current_streak: int = Field(ge=0)
    latest_score: float = Field(ge=0, le=100)
    current_difficulty: str


class LevelPredictionResponse(BaseModel):
    recommended_level: str
    confidence: float
    model_type: str
    explanation: str


app = FastAPI(
    title="PharmaTrainerAI ML Recommendation Service",
    description="ML microservice for predicting the next suitable training difficulty level",
    version="0.1.0",
)


def convert_difficulty_to_number(difficulty: str) -> int:
    difficulty_name = difficulty.strip().lower()

    if difficulty_name == "beginner":
        return 1

    if difficulty_name == "intermediate":
        return 2

    if difficulty_name == "advanced":
        return 3

    return 1


@app.get("/health")
def health_check():
    return {
        "status": "running",
        "service": "PharmaTrainerAI ML Recommendation Service",
        "model": "RandomForestClassifier",
    }


@app.post("/predict-level", response_model=LevelPredictionResponse)
def predict_next_level(request: LevelPredictionRequest):
    difficulty_number = convert_difficulty_to_number(request.current_difficulty)

    prediction = difficulty_model.predict_level(
        average_score=request.average_score,
        correct_rate=request.correct_rate,
        total_attempts=request.total_attempts,
        current_streak=request.current_streak,
        latest_score=request.latest_score,
        difficulty_number=difficulty_number,
    )

    return LevelPredictionResponse(
        recommended_level=prediction["recommended_level"],
        confidence=prediction["confidence"],
        model_type="RandomForestClassifier",
        explanation=(
            "The model predicted the next training level using average score, "
            "correct rate, total attempts, current streak, latest score, "
            "and current difficulty."
        ),
    )