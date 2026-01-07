from fast_agend.repositories.user_repository import UserRepository
from fast_agend.schemas import UserSchema
from fast_agend.models import User

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserSchema) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            cpf=user_data.cpf,
            phone=user_data.phone,
        )
        return self.repository.create(user)

    def list_users(self) -> list[User]:
        return self.repository.get_all()

    def update_user(self, user_id: int, user_data: UserSchema) -> User | None:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        user.username = user_data.username
        user.email = user_data.email
        user.password = user_data.password
        user.cpf = user_data.cpf
        user.phone = user_data.phone

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> User | None:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        self.repository.delete(user)
        return user
