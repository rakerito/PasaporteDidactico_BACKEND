from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pasaporte Didactico Backend"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Supabase settings
    SUPABASE_URL: str = "https://bvrzerkpmajajhdrahvn.supabase.co"
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_PUBLISHABLE_KEY: Optional[str] = "sb_publishable_3G84BteJ7e6Tfa8Qx3ADyg_HgEw3nqh"
    SUPABASE_SECRET_KEY: Optional[str] = None

    # Supabase table / schema configuration
    SUPABASE_SCHEMA: str = "public"
    SUPABASE_USUARIO: str = "usuario"

    @property
    def active_supabase_key(self) -> str:
        return self.SUPABASE_KEY or self.SUPABASE_PUBLISHABLE_KEY or ""

    @property
    def supabase_url(self) -> str:
        return self.SUPABASE_URL

    @property
    def supabase_key(self) -> str:
        return self.active_supabase_key

    @property
    def supabase_schema(self) -> str:
        return self.SUPABASE_SCHEMA

    @property
    def supabase_usuario(self) -> str:
        return self.SUPABASE_USUARIO

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
config = settings
