from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    supabase_jwt_secret: str

    # Database
    database_url: str

    # Google Cloud
    google_cloud_project: str = "fabpulse-prod"
    vertex_ai_location: str = "us-central1"
    gemini_model: str = "gemini-1.5-pro"

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_starter_price_id: str = ""
    stripe_growth_price_id: str = ""
    stripe_pro_price_id: str = ""

    # App
    app_url: str = "https://fabpulse.io"
    api_url: str = "https://api.fabpulse.io"
    environment: str = "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
