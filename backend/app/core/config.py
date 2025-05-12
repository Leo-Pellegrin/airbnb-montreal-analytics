from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    PGURL: str
    TEST_PGURL: Optional[str] = None
    JWTSECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 3600  # 1 hour
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ACCESS_TOKEN_EXPIRE_MINUTES_REFRESH: int = 60 * 24 * 30  # 30 days

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        # pytest injecte TEST_PGURL ; en prod c'est None -> on tombe sur PGURL
        return self.TEST_PGURL or self.PGURL


settings = Settings()
