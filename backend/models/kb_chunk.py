from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class KBChunk(BaseModel):
    tenant_id: str
    document_id: str
    document_name: str
    
    # Content
    text: str
    chunk_index: int
    
    # Embeddings (stored as list of floats)
    embedding: Optional[List[float]] = None
    
    # Metadata
    metadata: Dict[str, Any] = {}
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)


class KBChunkInDB(KBChunk):
    id: Optional[str] = Field(None, alias="_id")
    
    model_config = ConfigDict(populate_by_name=True)


class DocumentUpload(BaseModel):
    name: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    document_id: str
    name: str
    chunks_count: int
    created_at: datetime
