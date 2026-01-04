"""Configuration for Nexora SaaS Backend"""
import os
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "Nexora API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # Dodo Payments
    dodo_api_key: Optional[str] = None
    dodo_webhook_secret: Optional[str] = None
    dodo_api_url: str = "https://api.dodopayments.com"
    dodo_environment: str = "live_mode"  # or "test_mode"
    
    # Dodo Payments Product ID for pay-per-brief (one-time payment)
    dodo_product_brief: Optional[str] = None  # Product ID for pay-per-brief purchase
    
    # Brief pricing
    brief_price_usd: float = 3.00
    
    # CORS - accepts comma-separated string or list
    cors_origins: str = "http://localhost:3000"
    
    # API
    api_url: str = "https://api.nexora.io"
    
    # Engine
    engine_timeout_seconds: int = 300
    engine_max_retries: int = 2
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return self.cors_origins if isinstance(self.cors_origins, list) else []
    
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
