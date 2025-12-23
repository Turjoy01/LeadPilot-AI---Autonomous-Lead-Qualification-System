from fastapi import APIRouter, HTTPException
from backend.database import get_tenants_collection
from pydantic import BaseModel

router = APIRouter(prefix="/v1/widget", tags=["Widget"])


class WidgetConfig(BaseModel):
    tenant_name: str
    greeting: str
    brand_color: str
    language: str


@router.get("/config", response_model=WidgetConfig)
async def get_widget_config(tenant_key: str):
    """
    Get widget configuration for a tenant
    
    This endpoint is called when the widget loads
    
    **Example Request:**
    ```
    GET /v1/widget/config?tenant_key=demo-key-12345
    ```
    """
    try:
        # Get collection
        tenants_collection = get_tenants_collection()
        
        # Check if MongoDB collections are initialized
        if tenants_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        tenant_doc = await tenants_collection.find_one({"tenant_key": tenant_key})
        
        if not tenant_doc:
            raise HTTPException(status_code=404, detail="Invalid tenant key")
        
        from backend.models.tenant import Tenant
        if "_id" in tenant_doc:
            tenant_doc["id"] = str(tenant_doc.pop("_id"))
        tenant = Tenant(**tenant_doc)
        
        return WidgetConfig(
            tenant_name=tenant.name,
            greeting=tenant.settings.greeting,
            brand_color=tenant.settings.brand_color,
            language=tenant.settings.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting widget config: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
