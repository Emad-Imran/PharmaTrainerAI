# PharmaTrainerAI

## AI-Enhanced Gamified Training Platform for Smart Pharmaceutical Manufacturing

PharmaTrainerAI is a software architecture and design pattern project that combines Artificial Intelligence, gamification, and simulated pharmaceutical manufacturing scenarios.

The system allows users to solve decision-based manufacturing challenges, earn points and badges, track skill progress, view leaderboard rankings, and receive AI-based recommendations for the next suitable challenge based on their historical performance.

---

## Project Purpose

The main purpose of this project is to demonstrate how AI and gamification can be combined to create an adaptive learning and training platform for smart pharmaceutical manufacturing.

The platform focuses on simulated challenges related to:

- Process control
- Quality control
- Predictive maintenance
- Safety and compliance
- Packaging inspection

---

## Main Features

- User registration and login
- Dashboard with user progress
- Simulated pharmaceutical manufacturing scenarios
- Digital twin-style process parameters
- Scenario answer submission
- Scoring system
- Points, levels, streaks, and badges
- Skill progress tracking
- Leaderboard
- AI-based next challenge recommendation
- FastAPI Swagger documentation
- Dockerized deployment
- Design pattern implementation

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python FastAPI |
| UI | Jinja2 Templates + CSS |
| Database | SQLite for local prototype |
| ORM | SQLAlchemy |
| Authentication | Password hashing with Passlib |
| Containerization | Docker and Docker Compose |
| Documentation | Markdown |
| IDE | PyCharm |

---

## Architecture

The project follows a Modular Monolith architecture with Clean Architecture principles.

Main layers:

```text
UI Layer
FastAPI Route Layer
Service Layer
Repository Layer
Database Model Layer
Pattern Layer