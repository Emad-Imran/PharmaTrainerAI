from app.core.security import hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, full_name: str, email: str, password: str):
        existing_user = self.user_repository.find_by_email(email)

        if existing_user:
            return None

        secured_password = hash_password(password)

        return self.user_repository.create_user(
            full_name=full_name,
            email=email,
            hashed_password=secured_password
        )

    def login_user(self, email: str, password: str):
        user = self.user_repository.find_by_email(email)

        if not user:
            return None

        password_is_valid = verify_password(password, user.hashed_password)

        if not password_is_valid:
            return None

        return user