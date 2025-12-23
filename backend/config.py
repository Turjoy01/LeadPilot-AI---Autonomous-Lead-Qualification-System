from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    
    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_temperature: float = 0.7
    max_tokens: int = 1000
    
    # Email
    gmail_address: str = ""
    app_password: str = ""
    
    # JWT
    jwt_secret: str = "a1cede4693b6c5ba9a4e94d1b5b97957df6bb76d848f3b3188f6b8e7c3c18d5581f02cea16077c34b8d17427f738b3f95aaca6715c8d48e5888d4edc4f232689"  # Will be overridden by .env
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # Application
    environment: str = "development"
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:5173"
    
    # Default Tenant
    default_tenant_id: str = "default-tenant"
    default_tenant_name: str = "Demo Business"
    
    # Rate Limiting
    max_requests_per_minute: int = 60
    max_chat_messages_per_session: int = 100
    
    # Lead Scoring
    hot_lead_threshold: int = 70
    warm_lead_threshold: int = 40
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()
