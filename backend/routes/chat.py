from fastapi import APIRouter, HTTPException, Depends, Request
from backend.models.conversation import ChatRequest, ChatResponse, Conversation
from backend.models.lead import Lead
from backend.services.ai_agent import ai_agent
from backend.database import get_tenants_collection, get_conversations_collection, get_leads_collection
from backend.utils.rate_limiter import rate_limiter
from backend.config import settings
import uuid
from datetime import datetime

router = APIRouter(prefix="/v1/chat", tags=["Chat"])


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest, http_request: Request):
    """
    Public chat endpoint - handles user messages
    
    This is the main endpoint for the chat widget
    
    **Example Request:**
    ```json
    {
        "message": "Hello, I'm interested in your services",
        "session_id": "optional-session-id",
        "tenant_key": "demo-key-12345",
        "language": "en"
    }
    ```
    """
    try:
        # Get collections
        tenants_collection = get_tenants_collection()
        conversations_collection = get_conversations_collection()
        leads_collection = get_leads_collection()
        
        # Check if MongoDB collections are initialized
        if tenants_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Rate limiting
        client_ip = http_request.client.host
        rate_key = f"chat:{request.tenant_key}:{client_ip}"
        
        if not await rate_limiter.is_allowed(rate_key, settings.max_requests_per_minute):
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
        
        # Get tenant
        tenant_doc = await tenants_collection.find_one({"tenant_key": request.tenant_key})
        if not tenant_doc:
            raise HTTPException(status_code=404, detail="Invalid tenant key")
        
        from backend.models.tenant import Tenant
        if "_id" in tenant_doc:
            tenant_doc["id"] = str(tenant_doc.pop("_id"))
        tenant = Tenant(**tenant_doc)
        
        if not tenant.active:
            raise HTTPException(status_code=403, detail="Tenant is not active")
        
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get existing conversation
        conversation_doc = await conversations_collection.find_one({"session_id": session_id})
        if conversation_doc:
            if "_id" in conversation_doc:
                conversation_doc["id"] = str(conversation_doc.pop("_id"))
            conversation = Conversation(**conversation_doc)
        else:
            conversation = None
        
        # Get existing lead
        lead_doc = await leads_collection.find_one({"session_id": session_id})
        if lead_doc:
            if "_id" in lead_doc:
                lead_doc["id"] = str(lead_doc.pop("_id"))
            lead = Lead(**lead_doc)
        else:
            lead = None
        
        # Process message with AI agent
        response_message, updated_conversation, updated_lead, lead_became_hot = await ai_agent.process_message(
            request.message,
            session_id,
            tenant,
            conversation,
            lead
        )
        
        # Save conversation
        conversation_data = updated_conversation.model_dump(exclude={"id"})
        if conversation_doc:
            await conversations_collection.update_one(
                {"session_id": session_id},
                {"$set": conversation_data}
            )
        else:
            await conversations_collection.insert_one(conversation_data)
        
        # Save lead
        if updated_lead:
            lead_data = updated_lead.model_dump(exclude={"id"})
            if lead_doc:
                await leads_collection.update_one(
                    {"session_id": session_id},
                    {"$set": lead_data}
                )
            else:
                result = await leads_collection.insert_one(lead_data)
                # Update conversation with lead_id
                await conversations_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"lead_id": str(result.inserted_id)}}
                )
        
        # Prepare response
        return ChatResponse(
            message=response_message,
            session_id=session_id,
            lead_captured=updated_lead is not None,
            lead_grade=updated_lead.grade.value if updated_lead else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
