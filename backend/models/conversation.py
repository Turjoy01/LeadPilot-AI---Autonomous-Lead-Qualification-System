from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class Conversation(BaseModel):
    session_id: str
    tenant_id: str
    lead_id: Optional[str] = None
    
    # Messages
    messages: List[Message] = []
    
    # Summary for context management
    summary: Optional[str] = None
    
    # Metadata
    language: str = "en"
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationInDB(Conversation):
    id: Optional[str] = Field(None, alias="_id")
    
    model_config = ConfigDict(populate_by_name=True)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    tenant_key: str
    language: Optional[str] = "en"


class ChatResponse(BaseModel):
    message: str
    session_id: str
    lead_captured: bool = False
    lead_grade: Optional[str] = None
