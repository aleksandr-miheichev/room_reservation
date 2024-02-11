from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Бронирование переговорок'
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
