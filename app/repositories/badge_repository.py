from sqlalchemy.orm import Session

from app.models.badge import Badge
from app.models.user_badge import UserBadge


class BadgeRepository:
    def __init__(self, database: Session):
        self.database = database

    def count_badges(self):
        return self.database.query(Badge).count()

    def create_badge(
        self,
        name: str,
        description: str,
        category: str,
        required_correct_attempts: int,
    ):
        badge = Badge(
            name=name,
            description=description,
            category=category,
            required_correct_attempts=required_correct_attempts,
        )

        self.database.add(badge)
        self.database.commit()
        self.database.refresh(badge)

        return badge

    def find_all_badges(self):
        return self.database.query(Badge).order_by(Badge.id.asc()).all()

    def find_user_badges(self, user_id: int):
        return (
            self.database.query(UserBadge, Badge)
            .join(Badge, UserBadge.badge_id == Badge.id)
            .filter(UserBadge.user_id == user_id)
            .all()
        )

    def user_has_badge(self, user_id: int, badge_id: int) -> bool:
        existing_badge = (
            self.database.query(UserBadge)
            .filter(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge_id,
            )
            .first()
        )

        return existing_badge is not None

    def award_badge(self, user_id: int, badge_id: int):
        if self.user_has_badge(user_id=user_id, badge_id=badge_id):
            return None

        user_badge = UserBadge(
            user_id=user_id,
            badge_id=badge_id,
        )

        self.database.add(user_badge)
        self.database.commit()
        self.database.refresh(user_badge)

        return user_badge