"""
CinePulse Backend Configuration
Loads validated environment variables via Pydantic Settings.
"""
from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Server configuration
    ENVIRONMENT: str = Field(default="development")
    PORT: int = Field(default=8000)
    ALLOWED_ORIGINS: str = Field(default="http://localhost:3000,https://cinepulse.vercel.app")

    # NLP Artifacts path
    ARTIFACTS_DIR: str = Field(default="backend/app/recommender/artifacts")

    # Supabase credentials (Optional in local dev fallback mode)
    SUPABASE_URL: Optional[str] = Field(default=None)
    SUPABASE_ANON_KEY: Optional[str] = Field(default=None)
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = Field(default=None)
    SUPABASE_JWT_SECRET: Optional[str] = Field(default=None)

    # TMDB API (Optional for official posters/backdrops)
    TMDB_API_KEY: Optional[str] = Field(default=None)

    # Payments & Subscriptions
    PAYMENT_PROVIDER: str = Field(default="sandbox")  # sandbox, stripe, sslcommerz
    STRIPE_SECRET_KEY: Optional[str] = Field(default=None)
    STRIPE_WEBHOOK_SECRET: Optional[str] = Field(default=None)
    STRIPE_PRICE_PREMIUM: Optional[str] = Field(default="price_mock_premium")
    STRIPE_PRICE_PRO: Optional[str] = Field(default="price_mock_pro")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def resolved_artifacts_dir(self) -> Path:
        base = Path(__file__).resolve().parent.parent.parent
        p = base / self.ARTIFACTS_DIR
        return p if p.is_absolute() else (base / self.ARTIFACTS_DIR).resolve()

settings = Settings()
