from pydantic_settings import BaseSettings,SettingsConfigDict
from fastapi_mail import ConnectionConfig

class Settings(BaseSettings):
    TEST_DB: str
    DEV_DB: str
    SECRET_KEY_1:str
    ALGORITHM_1:str
    ACCESS_TOKEN_EXPIRE_1:int
    MAIL_USERNAME : str
    MAIL_PASSWORD :str
    model_config =  SettingsConfigDict(env_file=".env", extra="ignore")
settings=Settings()
conf= ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM="cousecomplete@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="E-Commerce",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
