# Architecture Overview

PharmaTrainerAI uses a Modular Monolith architecture with Clean Architecture principles.

## Main Layers

1. UI Layer  
   Jinja2 templates and CSS files render the user interface.

2. API Layer  
   FastAPI routes handle HTTP requests and responses.

3. Service Layer  
   Business logic is placed inside service classes.

4. Repository Layer  
   Database operations are isolated inside repository classes.

5. Model Layer  
   SQLAlchemy models define the database tables.

6. Pattern Layer  
   Design pattern implementations are stored inside the patterns directory.

## Why Modular Monolith?

A modular monolith is suitable for this academic prototype because it is easier to develop and test while still maintaining separation of concerns. Each module can later be separated into microservices if required.

## Main Modules

- Authentication Module
- Scenario Module
- Attempt and Scoring Module
- Gamification Module
- AI Recommendation Module
- Profile and Leaderboard Module