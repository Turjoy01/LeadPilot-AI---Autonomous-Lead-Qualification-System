from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from backend.models.kb_chunk import DocumentUpload, DocumentResponse
from backend.models.user import TokenData
from backend.database import get_kb_chunks_collection
from backend.services.kb_processor import KBProcessor
from backend.utils.auth import get_current_user
from datetime import datetime
from typing import List

router = APIRouter(prefix="/v1/knowledge-base", tags=["Knowledge Base"])

kb_processor = KBProcessor()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    document: DocumentUpload,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Upload a text document to knowledge base
    
    **Example Request:**
    ```json
    {
        "name": "Product Information",
        "content": "Our product is the best solution for your business needs..."
    }
    ```
    """
    try:
        # Get collection
        kb_chunks_collection = get_kb_chunks_collection()
        
        # Check if MongoDB collections are initialized
        if kb_chunks_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Add metadata
        if not document.metadata:
            document.metadata = {}
        document.metadata["uploaded_by"] = current_user.email
        
        # Process document
        document_id = await kb_processor.process_document(
            document,
            current_user.tenant_id
        )
        
        # Count chunks
        chunks_count = await kb_chunks_collection.count_documents({
            "document_id": document_id,
            "tenant_id": current_user.tenant_id
        })
        
        return DocumentResponse(
            document_id=document_id,
            name=document.name,
            chunks_count=chunks_count,
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        print(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/documents")
async def get_documents(current_user: TokenData = Depends(get_current_user)):
    """
    Get all documents in knowledge base
    
    **Example Request:**
    ```
    GET /v1/knowledge-base/documents
    ```
    """
    try:
        # Get collection
        kb_chunks_collection = get_kb_chunks_collection()
        
        # Check if MongoDB collections are initialized
        if kb_chunks_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Aggregate to get unique documents
        pipeline = [
            {"$match": {"tenant_id": current_user.tenant_id}},
            {
                "$group": {
                    "_id": "$document_id",
                    "name": {"$first": "$document_name"},
                    "chunks_count": {"$sum": 1},
                    "created_at": {"$first": "$created_at"}
                }
            },
            {"$sort": {"created_at": -1}}
        ]
        
        documents = []
        async for doc in kb_chunks_collection.aggregate(pipeline):
            documents.append({
                "document_id": doc["_id"],
                "name": doc["name"],
                "chunks_count": doc["chunks_count"],
                "created_at": doc["created_at"]
            })
        
        return documents
        
    except Exception as e:
        print(f"Error getting documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Delete a document from knowledge base
    
    **Example Request:**
    ```
    DELETE /v1/knowledge-base/documents/507f1f77bcf86cd799439011
    ```
    """
    try:
        await kb_processor.delete_document(document_id, current_user.tenant_id)
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        print(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats")
async def get_kb_stats(current_user: TokenData = Depends(get_current_user)):
    """
    Get knowledge base statistics
    
    **Example Request:**
    ```
    GET /v1/knowledge-base/stats
    ```
    
    **Example Response:**
    ```json
    {
        "total_documents": 5,
        "total_chunks": 120
    }
    ```
    """
    try:
        # Get collection
        kb_chunks_collection = get_kb_chunks_collection()
        
        # Check if MongoDB collections are initialized
        if kb_chunks_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        total_chunks = await kb_chunks_collection.count_documents({
            "tenant_id": current_user.tenant_id
        })
        
        # Count unique documents
        pipeline = [
            {"$match": {"tenant_id": current_user.tenant_id}},
            {"$group": {"_id": "$document_id"}},
            {"$count": "total"}
        ]
        
        result = await kb_chunks_collection.aggregate(pipeline).to_list(1)
        total_documents = result[0]["total"] if result else 0
        
        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks
        }
        
    except Exception as e:
        print(f"Error getting KB stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
