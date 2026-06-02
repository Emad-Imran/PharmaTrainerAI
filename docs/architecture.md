# Architecture Overview

PharmaTrainerAI uses a modular architecture with two Dockerized services.

## Services

### 1. Core Training Service

The Core Training Service is the main FastAPI application. It handles:

- User registration and login
- Scenario listing and scenario detail pages
- Attempt submission
- Scoring
- Gamification
- Mastery-based learning progression
- Profile and leaderboard
- AI recommendation page
- Communication with the ML service

### 2. ML Recommendation Service

The ML Recommendation Service is a separate FastAPI microservice. It uses a Scikit-learn RandomForestClassifier to predict the next suitable difficulty level.

The prediction classes are:

- Beginner
- Intermediate
- Advanced

---

## Architecture Diagram

```text
Browser / User
     |
     v
Core Training Service - FastAPI, Jinja2, SQLAlchemy
     |
     | HTTP request through Adapter Pattern
     v
ML Recommendation Service - FastAPI, Scikit-learn
     |
     v
Prediction: Beginner / Intermediate / Advanced