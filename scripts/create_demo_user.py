"""
Create a demo admin user for LeadPilot AI
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import connect_to_mongo, close_mongo_connection, get_users_collection
from backend.utils.auth import get_password_hash
from backend.config import settings


async def create_demo_user():
    """Create demo admin user"""
    await connect_to_mongo()
    
    try:
        # Get users collection
        users_collection = get_users_collection()
        
        if users_collection is None:
            print("✗ Error: Database not initialized properly")
            return
        
        # Check if user exists
        existing = await users_collection.find_one({"email": "admin@demo.com"})
        
        if existing:
            print("✓ Demo user already exists")
            print("  Email: admin@demo.com")
            print("  Password: demo123")
        else:
            # Create user
            user_data = {
                "email": "admin@demo.com",
                "full_name": "Demo Admin",
                "tenant_id": settings.default_tenant_id,
                "role": "admin",
                "hashed_password": get_password_hash("demo123"),
                "active": True
            }
            
            result = await users_collection.insert_one(user_data)
            
            print("✓ Demo user created successfully!")
            print("  Email: admin@demo.com")
            print("  Password: demo123")
            print("\nYou can now login to the admin dashboard at http://localhost:5173/login")
    
    except Exception as e:
        print(f"✗ Error creating demo user: {e}")
    
    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(create_demo_user())
