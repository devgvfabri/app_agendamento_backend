import re
from fast_agend.exceptions.user_exceptions import InvalidPasswordException 
def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    digito1 = 0 if digito1 == 10 else digito1

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    digito2 = 0 if digito2 == 10 else digito2

    return cpf[-2:] == f"{digito1}{digito2}"


def cpf_normalize(cpf: str) -> str:
    return re.sub(r'[^0-9]', '', cpf)

def validate_password(password: str) -> None:
    if len(password) < 8:
        raise InvalidPasswordException(
            "A senha deve ter pelo menos 8 caracteres."
        )

    if not re.search(r"[A-Z]", password):
        raise InvalidPasswordException(
            "A senha deve conter pelo menos uma letra maiúscula."
        )

    if not re.search(r"\d", password):
        raise InvalidPasswordException(
            "A senha deve conter pelo menos um número."
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise InvalidPasswordException(
            "A senha deve conter pelo menos um caractere especial."
        )