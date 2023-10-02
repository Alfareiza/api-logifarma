from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    PROJECT_NAME: str = "Api de Logifarma"

    DB_URL: str

    EMAILS_FROM_NAME: str
    EMAILS_FROM_EMAIL: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_SSL: str
    SMTP_USER: str
    SMTP_PASSWORD: str

    EMAIL_ADMIN: str

    EMAIL_TEMPLATES_DIR: str = "app/email-templates/base"

settings = Settings()