from typing import List
from openai import AsyncOpenAI
from backend.config import settings
from backend.models.kb_chunk import KBChunk, DocumentUpload
from backend.database import get_kb_chunks_collection
import uuid
from datetime import datetime

client = AsyncOpenAI(api_key=settings.openai_api_key)


class KBProcessor:
    """Knowledge base document processor"""
    
    def __init__(self):
        self.chunk_size = 1000  # characters
        self.chunk_overlap = 200  # characters
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Input text to chunk
        
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Get chunk
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move start with overlap
            start = end - self.chunk_overlap
            
            # Prevent infinite loop
            if start >= text_length or end >= text_length:
                break
        
        return chunks
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        """
        try:
            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    async def process_document(
        self,
        document: DocumentUpload,
        tenant_id: str
    ) -> str:
        """
        Process document: chunk and generate embeddings
        
        Args:
            document: Document to process
            tenant_id: Tenant ID
        
        Returns:
            Document ID
        """
        document_id = str(uuid.uuid4())
        
        # Chunk the document
        chunks = self.chunk_text(document.content)
        
        # Process each chunk
        for idx, chunk_text in enumerate(chunks):
            # Generate embedding
            embedding = await self.generate_embedding(chunk_text)
            
            # Create KB chunk
            kb_chunk = KBChunk(
                tenant_id=tenant_id,
                document_id=document_id,
                document_name=document.name,
                text=chunk_text,
                chunk_index=idx,
                embedding=embedding,
                metadata=document.metadata or {},
                created_at=datetime.utcnow()
            )
            
            # Insert into database
            kb_chunks_collection = get_kb_chunks_collection()
            if kb_chunks_collection is None:
                raise Exception("Database not initialized")
            
            await kb_chunks_collection.insert_one(kb_chunk.model_dump())
        
        return document_id
    
    async def delete_document(self, document_id: str, tenant_id: str):
        """Delete all chunks for a document"""
        kb_chunks_collection = get_kb_chunks_collection()
        if kb_chunks_collection is None:
            raise Exception("Database not initialized")
        
        await kb_chunks_collection.delete_many({
            "document_id": document_id,
            "tenant_id": tenant_id
        })
