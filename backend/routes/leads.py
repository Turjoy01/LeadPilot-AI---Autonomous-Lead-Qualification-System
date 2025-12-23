from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from backend.models.lead import LeadResponse, LeadUpdate, Lead, LeadStatus, LeadGrade
from backend.models.user import TokenData
from backend.database import get_leads_collection, get_conversations_collection
from backend.utils.auth import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/v1/leads", tags=["Leads"])


@router.get("", response_model=List[LeadResponse])
async def get_leads(
    status: Optional[LeadStatus] = None,
    grade: Optional[LeadGrade] = None,
    limit: int = Query(50, le=100),
    skip: int = 0,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Get leads for the current tenant with optional filters
    
    **Example Request:**
    ```
    GET /v1/leads?status=new&grade=HOT&limit=10&skip=0
    ```
    """
    try:
        # Get collection
        leads_collection = get_leads_collection()
        
        # Check if MongoDB collections are initialized
        if leads_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Build query
        query = {"tenant_id": current_user.tenant_id}
        
        if status:
            query["status"] = status.value
        if grade:
            query["grade"] = grade.value
        
        # Get leads
        cursor = leads_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        
        leads = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            leads.append(LeadResponse(**doc))
        
        return leads
        
    except Exception as e:
        print(f"Error getting leads: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{lead_id}")
async def get_lead(
    lead_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Get a specific lead with conversation transcript
    
    **Example Request:**
    ```
    GET /v1/leads/507f1f77bcf86cd799439011
    ```
    """
    try:
        # Get collections
        leads_collection = get_leads_collection()
        conversations_collection = get_conversations_collection()
        
        # Check if MongoDB collections are initialized
        if leads_collection is None or conversations_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Get lead
        lead_doc = await leads_collection.find_one({
            "_id": ObjectId(lead_id),
            "tenant_id": current_user.tenant_id
        })
        
        if not lead_doc:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Convert _id to id for Pydantic model
        if "_id" in lead_doc:
            lead_doc["id"] = str(lead_doc.pop("_id"))
        lead = Lead(**lead_doc)
        
        # Get conversation
        conversation_doc = await conversations_collection.find_one({
            "session_id": lead.session_id
        })
        
        conversation = None
        if conversation_doc:
            from backend.models.conversation import Conversation
            if "_id" in conversation_doc:
                conversation_doc["id"] = str(conversation_doc.pop("_id"))
            conversation = Conversation(**conversation_doc)
        
        return {
            "lead": lead,
            "conversation": conversation
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting lead: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{lead_id}")
async def update_lead(
    lead_id: str,
    update_data: LeadUpdate,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Update a lead (status, assignment, notes, tags)
    
    **Example Request:**
    ```json
    {
        "status": "contacted",
        "assigned_to": "sales@example.com",
        "notes": [{"note": "Follow up scheduled", "created_at": "2024-01-01T00:00:00"}],
        "tags": ["priority", "enterprise"]
    }
    ```
    """
    try:
        # Get collection
        leads_collection = get_leads_collection()
        
        # Check if MongoDB collections are initialized
        if leads_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Build update dict
        update_dict = {}
        if update_data.status is not None:
            update_dict["status"] = update_data.status.value
        if update_data.assigned_to is not None:
            update_dict["assigned_to"] = update_data.assigned_to
        if update_data.notes is not None:
            update_dict["notes"] = update_data.notes
        if update_data.tags is not None:
            update_dict["tags"] = update_data.tags
        
        update_dict["updated_at"] = datetime.utcnow()
        
        # Update lead
        result = await leads_collection.update_one(
            {
                "_id": ObjectId(lead_id),
                "tenant_id": current_user.tenant_id
            },
            {"$set": update_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return {"message": "Lead updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating lead: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats/summary")
async def get_lead_stats(current_user: TokenData = Depends(get_current_user)):
    """
    Get lead statistics for dashboard
    
    **Example Request:**
    ```
    GET /v1/leads/stats/summary
    ```
    
    **Example Response:**
    ```json
    {
        "total_leads": 150,
        "hot_leads": 25,
        "warm_leads": 60,
        "cold_leads": 65,
        "new_leads": 10
    }
    ```
    """
    try:
        # Get collection
        leads_collection = get_leads_collection()
        
        # Check if MongoDB collections are initialized
        if leads_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Total leads
        total_leads = await leads_collection.count_documents({"tenant_id": current_user.tenant_id})
        
        # Leads by grade
        hot_leads = await leads_collection.count_documents({
            "tenant_id": current_user.tenant_id,
            "grade": LeadGrade.HOT.value
        })
        warm_leads = await leads_collection.count_documents({
            "tenant_id": current_user.tenant_id,
            "grade": LeadGrade.WARM.value
        })
        cold_leads = await leads_collection.count_documents({
            "tenant_id": current_user.tenant_id,
            "grade": LeadGrade.COLD.value
        })
        
        # Leads by status
        new_leads = await leads_collection.count_documents({
            "tenant_id": current_user.tenant_id,
            "status": LeadStatus.NEW.value
        })
        
        return {
            "total_leads": total_leads,
            "hot_leads": hot_leads,
            "warm_leads": warm_leads,
            "cold_leads": cold_leads,
            "new_leads": new_leads
        }
        
    except Exception as e:
        print(f"Error getting lead stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
