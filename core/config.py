import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    TOKEN_EXPIRE_MINUTE: int = 60 * 24
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # CORS 허용 host
    CORS_ORIGINS: List[AnyHttpUrl] = []

    # CORS_ORIGINS 유효성 검사
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_oriign(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    DB_URL = "mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

    # 대소문자 구분 옵션
    class Config:
        case_sensitive = True


settings = Settings
