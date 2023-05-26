from typing import List, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "*"
    ]
    # allow any localhost port
    BACKEND_CORS_ORIGINS_REGEX: str = r"^(http://localhost:\d+|https://landing-page-p57ip5e6s-logicielshadaly.vercel.app)$"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # redis credentials
    REDISUSER: str = "" # faire en sorte d'utiliser dotenv
    REDISPASSWORD: str = ""
    REDISHOST: str = ""
    REDISPORT: str = ""


    @validator("REDISHOST", "REDISPORT")
    def check_redis(cls, v, field):
        if not v:
            raise ValueError(
                f"{field.name} must be defined. For local development, you can use the default value in your .env '{field.name}={field.default}'"
            )
        return v

    LOG_LEVEL: str = "info"

    @validator("LOG_LEVEL")
    def check_log_level(cls, v, field):
        if v not in ["debug", "info", "warning", "error", "critical"]:
            raise ValueError(
                f"{field.name} must be a standard log level. For local development, you can use the default value in your .env '{field.name}={field.default}'"
            )
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
