from typing import List, Optional
from openai import AsyncOpenAI
from backend.config import settings
from backend.database import get_kb_chunks_collection
from backend.models.kb_chunk import KBChunk

client = AsyncOpenAI(api_key=settings.openai_api_key)


class RAGService:
    """Retrieval-Augmented Generation service"""
    
    def __init__(self):
        self.top_k = 3  # Number of chunks to retrieve
    
    async def retrieve_relevant_chunks(
        self,
        query: str,
        tenant_id: str
    ) -> List[KBChunk]:
        """
        Retrieve relevant KB chunks for a query using vector similarity
        
        Args:
            query: User query
            tenant_id: Tenant ID for isolation
        
        Returns:
            List of relevant KB chunks
        """
        try:
            # Generate query embedding
            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            query_embedding = response.data[0].embedding
            
            # For now, we'll do a simple retrieval without vector search
            # In production, you'd use MongoDB Atlas Vector Search
            # This is a fallback that gets recent chunks
            kb_chunks_collection = get_kb_chunks_collection()
            if kb_chunks_collection is None:
                return []
            
            cursor = kb_chunks_collection.find(
                {"tenant_id": tenant_id}
            ).sort("created_at", -1).limit(self.top_k)
            
            chunks = []
            async for doc in cursor:
                chunks.append(KBChunk(**doc))
            
            return chunks
            
        except Exception as e:
            print(f"Error retrieving chunks: {e}")
            return []
    
    def build_context(self, chunks: List[KBChunk]) -> str:
        """
        Build context string from retrieved chunks
        
        Args:
            chunks: Retrieved KB chunks
        
        Returns:
            Context string
        """
        if not chunks:
            return ""
        
        context_parts = []
        for idx, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Context {idx}]\n{chunk.text}\n")
        
        return "\n".join(context_parts)
    
    def create_rag_system_message(self, context: str, tenant_name: str) -> str:
        """
        Create system message with RAG context and guardrails
        
        Args:
            context: Retrieved context
            tenant_name: Business name
        
        Returns:
            System message
        """
        if context:
            return f"""You are a helpful AI assistant for {tenant_name}.

IMPORTANT INSTRUCTIONS:
1. Answer questions ONLY based on the provided context below
2. If the answer is not in the context, say "I don't have that information right now, but I'd be happy to connect you with our team who can help."
3. Be conversational and friendly
4. Help qualify the lead by understanding their needs
5. When appropriate, ask for contact information (name, email, phone)
6. Ask about their budget, timeline, and specific service interests

CONTEXT:
{context}

Remember: Only use information from the context above. Do not make up information."""
        else:
            return f"""You are a helpful AI assistant for {tenant_name}.

Your role is to:
1. Have friendly conversations with potential customers
2. Understand their needs and interests
3. Collect their contact information (name, email, phone)
4. Ask about their budget, timeline, and service interests
5. Be helpful and professional

If asked about specific details you don't know, say "I'd be happy to connect you with our team who can provide detailed information about that."""
