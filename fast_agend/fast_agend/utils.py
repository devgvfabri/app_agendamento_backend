import re
from fast_agend.exceptions.user_exceptions import InvalidPasswordException 
import random
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

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

def send_verification_email(email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Confirme seu e-mail"
    msg["From"] = f"FastAgend <{os.getenv('SMTP_USER')}>"
    msg["To"] = email

    msg.set_content("Seu cliente de e-mail não suporta HTML.")

    msg.add_alternative(
        f"""
        <html>
            <body>
                <h2>Confirmação de e-mail</h2>
                <p>Seu código:</p>
                <h1>{code}</h1>
                <p>Expira em <strong>15 minutos</strong>.</p>
            </body>
        </html>
        """,
        subtype="html",
    )

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(
            os.getenv("SMTP_USER"),
            os.getenv("SMTP_PASSWORD"),
        )
        server.send_message(msg)