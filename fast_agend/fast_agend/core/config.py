from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -------- FRONTEND --------
    FRONTEND_URL: str = "http://localhost:3000"

    # -------- SMTP / EMAIL --------
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    MAIL_FROM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()