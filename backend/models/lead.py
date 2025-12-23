from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class LeadGrade(str, Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"
    UNQUALIFIED = "UNQUALIFIED"


class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    WON = "won"
    LOST = "lost"


class LeadFields(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    service_interest: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None


class ScoreHistory(BaseModel):
    score: int
    grade: LeadGrade
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reason: Optional[str] = None


class Lead(BaseModel):
    tenant_id: str
    conversation_id: str
    session_id: str
    
    # Extracted fields
    fields: LeadFields = Field(default_factory=LeadFields)
    
    # Scoring
    score: int = 0
    grade: LeadGrade = LeadGrade.UNQUALIFIED
    score_history: List[ScoreHistory] = []
    
    # Status
    status: LeadStatus = LeadStatus.NEW
    assigned_to: Optional[str] = None
    
    # Notes and tags
    notes: List[Dict[str, Any]] = []
    tags: List[str] = []
    
    # Metadata
    source: str = "chat_widget"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_contact_at: Optional[datetime] = None


class LeadInDB(Lead):
    id: Optional[str] = Field(None, alias="_id")
    
    model_config = ConfigDict(populate_by_name=True)


class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    assigned_to: Optional[str] = None
    notes: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[str]] = None


class LeadResponse(BaseModel):
    id: str
    tenant_id: str
    fields: LeadFields
    score: int
    grade: LeadGrade
    status: LeadStatus
    assigned_to: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime
