from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from backend.config import settings
from backend.models.conversation import Message, Conversation
from backend.models.lead import Lead, LeadFields, LeadGrade
from backend.models.tenant import Tenant
from backend.services.rag_service import RAGService
from backend.services.lead_extraction import LeadExtractionService
from backend.services.lead_scoring import LeadScoringEngine
from backend.services.email_service import email_service
from backend.database import get_conversations_collection, get_leads_collection
from datetime import datetime
import uuid

client = AsyncOpenAI(api_key=settings.openai_api_key)


class AIAgent:
    """Core AI agent for lead qualification conversations"""
    
    def __init__(self):
        self.rag_service = RAGService()
        self.lead_extractor = LeadExtractionService()
        self.scoring_engine = LeadScoringEngine()
    
    async def process_message(
        self,
        user_message: str,
        session_id: str,
        tenant: Tenant,
        conversation: Optional[Conversation] = None,
        lead: Optional[Lead] = None
    ) -> tuple[str, Conversation, Optional[Lead], bool]:
        """
        Process user message and generate response
        
        Args:
            user_message: User's message
            session_id: Session ID
            tenant: Tenant object
            conversation: Existing conversation or None
            lead: Existing lead or None
        
        Returns:
            Tuple of (response_message, updated_conversation, updated_lead, lead_became_hot)
        """
        # Initialize conversation if new
        if not conversation:
            conversation = Conversation(
                session_id=session_id,
                tenant_id=tenant.tenant_id,
                messages=[],
                language=tenant.settings.language
            )
        
        # Add user message
        user_msg = Message(role="user", content=user_message)
        conversation.messages.append(user_msg)
        
        # Retrieve relevant KB chunks
        kb_chunks = await self.rag_service.retrieve_relevant_chunks(
            user_message,
            tenant.tenant_id
        )
        
        # Build context
        context = self.rag_service.build_context(kb_chunks)
        
        # Create system message with RAG context
        system_message = self.rag_service.create_rag_system_message(
            context,
            tenant.name
        )
        
        # Prepare messages for OpenAI
        openai_messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add conversation history (last 10 messages)
        for msg in conversation.messages[-10:]:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Generate response
        try:
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=openai_messages,
                temperature=settings.openai_temperature,
                max_tokens=settings.max_tokens
            )
            
            assistant_message = response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            assistant_message = "I apologize, but I'm having trouble processing your request right now. Please try again."
        
        # Add assistant message
        assistant_msg = Message(role="assistant", content=assistant_message)
        conversation.messages.append(assistant_msg)
        conversation.last_message_at = datetime.utcnow()
        
        # Extract lead information
        current_fields = lead.fields if lead else LeadFields()
        updated_fields = await self.lead_extractor.extract_from_conversation(
            [{"role": m.role, "content": m.content} for m in conversation.messages],
            current_fields
        )
        
        # Update or create lead
        lead_became_hot = False
        if updated_fields and updated_fields != current_fields:
            # Calculate conversation signals
            conversation_signals = {
                "message_count": len(conversation.messages) // 2,  # User messages
                "intent_keywords": self._extract_intent_keywords(user_message)
            }
            
            # Calculate new score
            new_score, new_grade = self.scoring_engine.calculate_score(
                updated_fields,
                conversation_signals
            )
            
            if not lead:
                # Create new lead
                lead = Lead(
                    tenant_id=tenant.tenant_id,
                    conversation_id=str(conversation.id) if hasattr(conversation, 'id') else session_id,
                    session_id=session_id,
                    fields=updated_fields,
                    score=new_score,
                    grade=new_grade
                )
                
                # Check if hot lead
                if new_grade == LeadGrade.HOT:
                    lead_became_hot = True
            else:
                # Update existing lead
                old_grade = lead.grade
                lead.fields = updated_fields
                lead.score = new_score
                lead.grade = new_grade
                lead.updated_at = datetime.utcnow()
                
                # Check if became hot
                if old_grade != LeadGrade.HOT and new_grade == LeadGrade.HOT:
                    lead_became_hot = True
            
            # Add score history
            score_entry = self.scoring_engine.create_score_history_entry(
                new_score,
                new_grade,
                "Updated from conversation"
            )
            lead.score_history.append(score_entry)
        
        # Send hot lead notification
        if lead_became_hot and lead:
            conversation_snippet = self._format_conversation_snippet(conversation.messages[-6:])
            await email_service.send_hot_lead_notification(
                lead,
                conversation_snippet,
                tenant.name,
                tenant.settings.notification_emails
            )
        
        return assistant_message, conversation, lead, lead_became_hot
    
    def _extract_intent_keywords(self, message: str) -> List[str]:
        """Extract intent keywords from message"""
        intent_keywords = ["pricing", "price", "cost", "quote", "buy", "purchase", "demo", "trial", "signup", "sign up"]
        message_lower = message.lower()
        return [kw for kw in intent_keywords if kw in message_lower]
    
    def _format_conversation_snippet(self, messages: List[Message]) -> str:
        """Format conversation for email"""
        lines = []
        for msg in messages:
            role = "Customer" if msg.role == "user" else "AI Assistant"
            lines.append(f"<p><strong>{role}:</strong> {msg.content}</p>")
        return "\n".join(lines)


# Global AI agent instance
ai_agent = AIAgent()
