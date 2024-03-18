from typing import Any
from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://....@......"
    SECRET_KEY_JWT: str = "drgf453e4td3edt4fdtr"
    ALGORITHM: str = "HS256"
    
    MAIL_USERNAME: EmailStr = "qwes@scfx.we"
    MAIL_PASSWORD: str = "qwerty@i.ua"
    MAIL_FROM: str = "qwes@scfx.we"
    MAIL_PORT: int = 3243
    MAIL_SERVER: str = "qwery.com.ua"

    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASS: str|None = None  

    CLOUD_NAME:str = "hw13"
    CLOUD_API_KEY:int = 691853932645285
    CLOUD_API_SECRET:str = "secret"

    
    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls,v:Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algo must be hs256 | hs512")
        return v


    model_config=  ConfigDict(extra="ignore", env_file = ".env", env_file_encoding = "utf-8") # type: ignore


config = Settings()

