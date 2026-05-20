# Design Patterns Used

## 1. Singleton Pattern

File: `app/core/config.py`

The application configuration is loaded using a cached settings function. This ensures that configuration is created once and reused.

## 2. Repository Pattern

Folder: `app/repositories`

Database access is separated from business logic. Each repository handles one database concern such as users, scenarios, attempts, badges, skills, or recommendations.

## 3. Strategy Pattern

File: `app/patterns/scoring_strategy.py`

Different scoring strategies are used depending on scenario difficulty. Beginner scenarios can use a practice scoring strategy, while other scenarios use standard scoring.

## 4. Adapter Pattern

File: `app/patterns/ai_recommendation_adapter.py`

The AI recommendation engine uses an adapter interface. The current implementation is rule-based, but it can later be replaced with a machine learning model or external AI service.

## 5. Observer Pattern

File: `app/patterns/gamification_observer.py`

After a scenario attempt, multiple observers update different parts of the gamification system:
- points
- streaks
- skill scores
- badges

## 6. Facade Pattern

File: `app/patterns/submission_facade.py`

The scenario submission workflow is simplified through one facade class. The route does not need to manage all repositories and services manually.

## 7. Factory Pattern

File: `app/patterns/scenario_factory.py`

The factory creates scenario category metadata used in the scenario detail page. This separates category creation logic from route and template logic.