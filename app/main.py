from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import SessionLocal, get_database_session
from app.core.init_db import create_database_tables

from app.repositories.user_repository import UserRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.attempt_repository import AttemptRepository

from app.services.auth_service import AuthService
from app.services.scenario_service import ScenarioService
from app.services.attempt_service import AttemptService
from app.repositories.badge_repository import BadgeRepository
from app.repositories.skill_score_repository import SkillScoreRepository
from app.services.gamification_service import GamificationService

from app.repositories.recommendation_repository import RecommendationRepository
from app.services.recommendation_service import RuleBasedRecommendationService
""" The below is the Facade Pattern Library"""
from app.patterns.submission_facade import ScenarioSubmissionFacade
""" The below is the Factory Pattern Library"""
from app.patterns.scenario_factory import ScenarioCategoryFactory

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.on_event("startup")
def on_application_startup():
    create_database_tables()

    database = SessionLocal()
    try:
        scenario_repository = ScenarioRepository(database)
        scenario_service = ScenarioService(scenario_repository)
        scenario_service.seed_default_scenarios()

        badge_repository = BadgeRepository(database)
        attempt_repository = AttemptRepository(database)
        user_repository = UserRepository(database)
        skill_score_repository = SkillScoreRepository(database)

        gamification_service = GamificationService(
            user_repository=user_repository,
            scenario_repository=scenario_repository,
            attempt_repository=attempt_repository,
            badge_repository=badge_repository,
            skill_score_repository=skill_score_repository,
        )

        gamification_service.seed_default_badges()

    finally:
        database.close()

@app.get("/")
def show_home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"project_name": settings.app_name},
    )


@app.get("/register")
def show_register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={},
    )


@app.post("/register")
def register_user(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    database: Session = Depends(get_database_session),
):
    user_repository = UserRepository(database)
    auth_service = AuthService(user_repository)

    created_user = auth_service.register_user(
        full_name=full_name,
        email=email,
        password=password,
    )

    if not created_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "This email is already registered."},
        )

    return RedirectResponse(url="/login", status_code=303)


@app.get("/login")
def show_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@app.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    database: Session = Depends(get_database_session),
):
    user_repository = UserRepository(database)
    auth_service = AuthService(user_repository)

    user = auth_service.login_user(email=email, password=password)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password."},
        )

    return RedirectResponse(url=f"/dashboard/{user.id}", status_code=303)


@app.get("/dashboard/{user_id}")
def show_dashboard(
    request: Request,
    user_id: int,
    database: Session = Depends(get_database_session),
):
    user_repository = UserRepository(database)
    user = user_repository.find_by_id(user_id)

    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"user": user},
    )


@app.get("/scenarios")
def show_scenarios(
    request: Request,
    database: Session = Depends(get_database_session),
):
    scenario_repository = ScenarioRepository(database)
    scenario_service = ScenarioService(scenario_repository)

    scenarios = scenario_service.get_all_scenarios()

    return templates.TemplateResponse(
        request=request,
        name="scenarios.html",
        context={"scenarios": scenarios},
    )


@app.get("/scenarios/{scenario_id}")
def show_scenario_detail(
    request: Request,
    scenario_id: int,
    database: Session = Depends(get_database_session),
):
    scenario_repository = ScenarioRepository(database)
    scenario_service = ScenarioService(scenario_repository)

    scenario = scenario_service.get_scenario_by_id(scenario_id)

    if not scenario:
        return RedirectResponse(url="/scenarios", status_code=303)

    parameter_items = [
        item.strip()
        for item in scenario.process_parameters.split("|")
    ]
    category_info = ScenarioCategoryFactory.create_category(scenario.category)

    return templates.TemplateResponse(
        request=request,
        name="scenario_detail.html",
        context={
            "scenario": scenario,
            "parameter_items": parameter_items,
            "category_info": category_info,
        },
    )


@app.get("/scenarios/{scenario_id}/attempt")
def redirect_attempt_get_request(scenario_id: int):
    return RedirectResponse(url=f"/scenarios/{scenario_id}", status_code=303)

@app.post("/scenarios/{scenario_id}/attempt")
def submit_scenario_attempt(
    scenario_id: int,
    user_id: int = Form(...),
    selected_option: str = Form(...),
    database: Session = Depends(get_database_session),
):
    submission_facade = ScenarioSubmissionFacade(database)

    attempt = submission_facade.submit_answer(
        user_id=user_id,
        scenario_id=scenario_id,
        selected_option=selected_option,
    )

    if not attempt:
        return RedirectResponse(url="/scenarios", status_code=303)

    return RedirectResponse(
        url=f"/attempts/{attempt.id}/result",
        status_code=303,
    )

@app.get("/attempts/{attempt_id}/result")
def show_attempt_result(
    request: Request,
    attempt_id: int,
    database: Session = Depends(get_database_session),
):
    attempt_repository = AttemptRepository(database)
    scenario_repository = ScenarioRepository(database)
    user_repository = UserRepository(database)

    attempt = attempt_repository.find_by_id(attempt_id)

    if not attempt:
        return RedirectResponse(url="/scenarios", status_code=303)

    scenario = scenario_repository.find_by_id(attempt.scenario_id)
    user = user_repository.find_by_id(attempt.user_id)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "attempt": attempt,
            "scenario": scenario,
            "user": user,
        },
    )
@app.get("/profile/{user_id}")
def show_profile(
    request: Request,
    user_id: int,
    database: Session = Depends(get_database_session),
):
    user_repository = UserRepository(database)
    badge_repository = BadgeRepository(database)
    skill_score_repository = SkillScoreRepository(database)
    attempt_repository = AttemptRepository(database)

    user = user_repository.find_by_id(user_id)

    if not user:
        return RedirectResponse(url="/login", status_code=303)

    earned_badges = badge_repository.find_user_badges(user_id=user_id)
    skill_scores = skill_score_repository.find_by_user(user_id=user_id)
    recent_attempts = attempt_repository.find_by_user(user_id=user_id)

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "user": user,
            "earned_badges": earned_badges,
            "skill_scores": skill_scores,
            "recent_attempts": recent_attempts[:5],
        },
    )
@app.get("/leaderboard")
def show_leaderboard(
    request: Request,
    database: Session = Depends(get_database_session),
):
    user_repository = UserRepository(database)
    users = user_repository.find_top_users(limit=10)

    return templates.TemplateResponse(
        request=request,
        name="leaderboard.html",
        context={"users": users},
    )

    return templates.TemplateResponse(
        request=request,
        name="leaderboard.html",
        context={"users": users},
    )

@app.get("/recommendation/{user_id}")
def show_ai_recommendation(
    request: Request,
    user_id: int,
    database: Session = Depends(get_database_session),
):
    user_repository = UserRepository(database)
    scenario_repository = ScenarioRepository(database)
    skill_score_repository = SkillScoreRepository(database)
    recommendation_repository = RecommendationRepository(database)

    user = user_repository.find_by_id(user_id)

    if not user:
        return RedirectResponse(url="/login", status_code=303)

    recommendation_service = RuleBasedRecommendationService(
        skill_score_repository=skill_score_repository,
        scenario_repository=scenario_repository,
        recommendation_repository=recommendation_repository,
    )

    recommendation = recommendation_service.recommend_next_scenario(user_id=user_id)

    if not recommendation:
        return RedirectResponse(url="/scenarios", status_code=303)

    scenario = scenario_repository.find_by_id(recommendation.scenario_id)

    return templates.TemplateResponse(
        request=request,
        name="recommendation.html",
        context={
            "user": user,
            "recommendation": recommendation,
            "scenario": scenario,
        },
    )

@app.get("/health")
def health_check():
    return {
        "status": "running",
        "service": settings.app_name,
        "version": settings.app_version,
        "message": "Attempt and scoring module is active.",
    }