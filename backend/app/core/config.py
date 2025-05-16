from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    PGURL: str
    TEST_PGURL: Optional[str] = None

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
