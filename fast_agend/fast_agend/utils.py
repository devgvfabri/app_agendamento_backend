import re
from fast_agend.exceptions.user_exceptions import InvalidPasswordException 
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

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

def generate_code():
        return str(random.randint(100000, 999999))

def send_verification_email(to_email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Verificação de e-mail"
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.set_content(f"Seu código de verificação é: {code}")
    print(SMTP_HOST)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)