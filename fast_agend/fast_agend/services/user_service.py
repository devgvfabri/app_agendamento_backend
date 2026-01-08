from fast_agend.repositories.user_repository import UserRepository
from fast_agend.schemas import UserSchema
from fast_agend.models import User
from fast_agend.utils import validar_cpf, cpf_normalize
from fast_agend.exceptions.user_exceptions import InvalidCPFException, ExistingNumberException, UsernameAlreadyExistsException
from fast_agend.exceptions.user_exceptions import EmailAlreadyExistsException, CPFAlreadyExistsException

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserSchema) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            cpf=cpf_normalize(user_data.cpf),
            phone=user_data.phone,
        )
        if not validar_cpf(user.cpf):
            raise InvalidCPFException()
        
        phone_owner = self.repository.get_by_phone(user_data.phone)
        if phone_owner:
            raise ExistingNumberException()

        username_owner = self.repository.get_by_username(user_data.username)
        if username_owner:
            raise UsernameAlreadyExistsException()

        cpf_owner = self.repository.get_by_cpf(user_data.cpf)
        if cpf_owner:
            raise CPFAlreadyExistsException()

        email_owner = self.repository.get_by_email(user_data.email)
        if email_owner:
            raise EmailAlreadyExistsException()

        return self.repository.create(user)

    def list_users(self) -> list[User]:
        return self.repository.get_all()

    def update_user(self, user_id: int, user_data: UserSchema) -> User | None:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        
        if not validar_cpf(user.cpf):
            raise InvalidCPFException()

        phone_owner = self.repository.get_by_phone(user_data.phone)
        if phone_owner and phone_owner.id != user_id:
            raise ExistingNumberException()

        user.username = user_data.username
        user.email = user_data.email
        user.password = user_data.password
        user.cpf = cpf_normalize(user_data.cpf)
        user.phone = user_data.phone

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> User | None:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        self.repository.delete(user)
        return user
