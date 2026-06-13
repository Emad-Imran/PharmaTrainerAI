# PharmaTrainerAI

## ML-Enhanced Adaptive Gamified Training Platform for Smart Pharmaceutical Manufacturing

PharmaTrainerAI is a Software Architecture and Design Pattern project focused on adaptive training for pharmaceutical manufacturing. The system combines gamification, mastery-based learning, and a machine learning classification model to recommend the next suitable training level for a user.

The platform is designed as a two-service application:

1. **Core Training Service**  
   Handles users, scenarios, attempts, scoring, gamification, mastery progress, UI pages, and database operations.

2. **ML Recommendation Service**  
   Uses a Scikit-learn classification model to predict the next suitable learning level: Beginner, Intermediate, or Advanced.

---

## Project Purpose

The goal of this project is to build an adaptive learning platform where a trainee progresses through pharmaceutical manufacturing scenarios in a structured way.

The user starts from the Beginner level. If the user answers incorrectly, the system detects the weak area and shows corrective learning guidance based on the selected research papers. The user cannot randomly jump to higher levels. Intermediate and Advanced levels unlock only after mastery of the previous level.

After completing Advanced level, the system unlocks industry exposure guidance and suggests relevant pharmaceutical manufacturing departments.

---

## Main Features

- User registration and login
- Adaptive scenario-based training
- Beginner, Intermediate, and Advanced learning levels
- Locked level progression
- Mastery-based learning path
- Weak-area detection after incorrect answers
- Research-paper-based learning hints
- ML-based difficulty recommendation
- Separate ML recommendation microservice
- Gamification with points, levels, streaks, badges, and leaderboard
- Profile page with progress tracking
- Industry exposure unlock after Advanced mastery
- Docker Compose setup for two services
- Design pattern implementation

---

## Machine Learning Component

The project includes a separate ML microservice built with FastAPI and Scikit-learn.

### Model Used

```text
RandomForestClassifier