from fast_agend.repositories.user_repository import UserRepository
from fast_agend.schemas import UserSchema, UserCreate, UserUpdateSchema
from fast_agend.models import User
from fast_agend.utils import validar_cpf, cpf_normalize, validate_password
from fast_agend.exceptions.user_exceptions import InvalidCPFException, ExistingNumberException, UsernameAlreadyExistsException
from fast_agend.exceptions.user_exceptions import EmailAlreadyExistsException, CPFAlreadyExistsException, InvalidCPFException
from fast_agend.security.password import hash_password
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fast_agend.security.password import SECRET_KEY, ALGORITHM
from fast_agend.security.password import oauth2_scheme

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> User:
        validate_password(user_data.password)

        cpf = cpf_normalize(user_data.cpf)
        if not validar_cpf(cpf):
            raise InvalidCPFException()

        if self.repository.get_by_phone(user_data.phone):
            raise ExistingNumberException()

        if self.repository.get_by_username(user_data.username):
            raise UsernameAlreadyExistsException()

        if self.repository.get_by_cpf(cpf):
            raise CPFAlreadyExistsException()

        if self.repository.get_by_email(user_data.email):
            raise EmailAlreadyExistsException()

        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password),  
            cpf=cpf,
            phone=user_data.phone,
        )

        return self.repository.create(user)

    def list_users(self) -> list[User]:
        return self.repository.get_all()

    def update_user(self, user_id: int, user_data: UserUpdateSchema) -> User | None:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        data = user_data.model_dump(exclude_unset=True)

        if "password" in data:
            validate_password(data["password"])
            user.password = hash_password(data["password"])

        if "username" in data:
            username_owner = self.repository.get_by_username(data["username"])
            if username_owner and username_owner.id != user_id:
                raise UsernameAlreadyExistsException()
            user.username = data["username"]

        if "cpf" in data:
            cpf = cpf_normalize(data["cpf"])

            if not validar_cpf(cpf):
                raise InvalidCPFException()

            cpf_owner = self.repository.get_by_cpf(cpf)
            if cpf_owner and cpf_owner.id != user_id:
                raise CPFAlreadyExistsException()

            user.cpf = cpf

        if "email" in data:
            email_owner = self.repository.get_by_email(data["email"])
            if email_owner and email_owner.id != user_id:
                raise EmailAlreadyExistsException()
            user.email = data["email"]

        if "phone" in data:
            phone_owner = self.repository.get_by_phone(data["phone"])
            if phone_owner and phone_owner.id != user_id:
                raise ExistingNumberException()

            user.phone = data["phone"]

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> User | None:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        self.repository.delete(user)
        return user

    def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")

            if not username:
                raise HTTPException(status_code=401, detail="Token inválido")

        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return user
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)