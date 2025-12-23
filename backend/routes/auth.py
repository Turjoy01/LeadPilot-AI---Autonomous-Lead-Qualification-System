from fastapi import APIRouter, HTTPException, Depends
from backend.models.user import UserLogin, Token, UserCreate, UserInDB
from backend.database import get_users_collection
from backend.utils.auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from backend.config import settings

router = APIRouter(prefix="/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login endpoint - returns JWT token
    
    **Example Request:**
    ```json
    {
        "email": "admin@demo.com",
        "password": "demo123"
    }
    ```
    """
    try:
        # Get collection
        users_collection = get_users_collection()
        
        # Check if MongoDB collections are initialized
        if users_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Find user
        user_doc = await users_collection.find_one({"email": credentials.email})
        
        if not user_doc:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Convert _id to id for Pydantic model
        if "_id" in user_doc:
            user_doc["id"] = str(user_doc.pop("_id"))
        user = UserInDB(**user_doc)
        
        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Check if active
        if not user.active:
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "tenant_id": user.tenant_id},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        return Token(access_token=access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """
    Register new user (admin only in production)
    
    **Example Request:**
    ```json
    {
        "email": "user@example.com",
        "password": "securepassword123",
        "full_name": "John Doe",
        "tenant_id": "default-tenant",
        "role": "admin"
    }
    ```
    """
    try:
        # Get collection
        users_collection = get_users_collection()
        
        # Check if MongoDB collections are initialized
        if users_collection is None:
            raise HTTPException(status_code=503, detail="Database not initialized. Please check MongoDB connection.")
        
        # Check if user exists
        existing = await users_collection.find_one({"email": user_data.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = UserInDB(
            email=user_data.email,
            full_name=user_data.full_name,
            tenant_id=user_data.tenant_id,
            role=user_data.role,
            hashed_password=hashed_password,
            active=True
        )
        
        # Insert into database
        await users_collection.insert_one(user.model_dump(exclude={"id"}))
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "tenant_id": user.tenant_id}
        )
        
        return Token(access_token=access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
