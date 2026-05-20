from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, database: Session):
        self.database = database

    def find_by_email(self, email: str):
        return self.database.query(User).filter(User.email == email).first()

    def find_by_id(self, user_id: int):
        return self.database.query(User).filter(User.id == user_id).first()

    def create_user(self, full_name: str, email: str, hashed_password: str):
        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password
        )

        self.database.add(user)
        self.database.commit()
        self.database.refresh(user)

        return user

    def add_points(self, user_id: int, points: int):
        user = self.find_by_id(user_id)

        if not user:
            return None

        user.total_points += points

        if user.total_points >= 500:
            user.current_level = "Advanced"
        elif user.total_points >= 250:
            user.current_level = "Intermediate"
        else:
            user.current_level = "Beginner"

        self.database.commit()
        self.database.refresh(user)

        return user

    def update_streak(self, user_id: int, is_correct: bool):
        user = self.find_by_id(user_id)

        if not user:
            return None

        if is_correct:
            user.current_streak += 1
        else:
            user.current_streak = 0

        self.database.commit()
        self.database.refresh(user)

        return user
    def find_top_users(self, limit: int = 10):
        return (
            self.database.query(User)
            .order_by(User.total_points.desc())
            .limit(limit)
            .all()
        )