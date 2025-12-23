from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class TenantSettings(BaseModel):
    greeting: str = "Hi! I'm here to help you. What can I assist you with today?"
    lead_questions: List[str] = []
    hot_threshold: int = 70
    warm_threshold: int = 40
    notification_emails: List[str] = []
    brand_color: str = "#6366f1"
    language: str = "en"


class Tenant(BaseModel):
    tenant_id: str
    tenant_key: str
    name: str
    email: str
    settings: TenantSettings
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TenantInDB(Tenant):
    id: Optional[str] = Field(None, alias="_id")
    
    model_config = ConfigDict(populate_by_name=True)
