from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, TEXT
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

# MongoDB client
client: AsyncIOMotorClient = None
db = None

# Collections
tenants_collection = None
users_collection = None
leads_collection = None
conversations_collection = None
kb_chunks_collection = None
events_collection = None


async def connect_to_mongo():
    """Connect to MongoDB and initialize collections"""
    global client, db
    global tenants_collection, users_collection, leads_collection
    global conversations_collection, kb_chunks_collection, events_collection
    
    try:
        # Connect to MongoDB
        # Increase timeout for MongoDB Atlas
        client = AsyncIOMotorClient(
            settings.mongodb_uri, 
            serverSelectionTimeoutMS=30000,  # 30 seconds for Atlas
            connectTimeoutMS=30000
        )
        
        # Extract database name from URI or use default
        # MongoDB Atlas URI format: mongodb+srv://user:pass@cluster/dbname?options
        uri_parts = settings.mongodb_uri.split('/')
        if len(uri_parts) > 3 and uri_parts[3]:
            # Database name is in URI (before ?)
            db_name = uri_parts[3].split('?')[0]
            if db_name:
                db = client.get_database(db_name)
            else:
                db = client.leadpilot_db
        else:
            # Use default database name
            db = client.leadpilot_db
        
        # Test connection
        await client.admin.command('ping')
        logger.info("MongoDB connection successful")
        
        # Initialize collections
        tenants_collection = db.tenants
        users_collection = db.users
        leads_collection = db.leads
        conversations_collection = db.conversations
        kb_chunks_collection = db.kb_chunks
        events_collection = db.events
        
        # Verify collections are initialized
        if tenants_collection is None:
            raise Exception("Failed to initialize tenants_collection")
        
        # Double check - verify we can access the collection
        test_count = await tenants_collection.count_documents({})
        logger.info(f"Verified tenants collection access - found {test_count} documents")
        
        # Create indexes
        await create_indexes()
        
        logger.info("Successfully connected to MongoDB and initialized collections")
        logger.info(f"Verified tenants collection access - found {test_count} documents")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        logger.error(f"MongoDB URI: {settings.mongodb_uri}")
        # Reset collections to None on error
        tenants_collection = None
        users_collection = None
        leads_collection = None
        conversations_collection = None
        kb_chunks_collection = None
        events_collection = None
        logger.error("Please ensure MongoDB Atlas is accessible and the URI is correct")
        logger.error("The application will start but API endpoints will return 503 errors")
        # Don't raise - allow app to start


async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        logger.info("Closed MongoDB connection")


async def create_indexes():
    """Create database indexes for performance"""
    try:
        # Tenants indexes
        await tenants_collection.create_index([("tenant_key", ASCENDING)], unique=True)
        
        # Users indexes
        await users_collection.create_index([("email", ASCENDING)], unique=True)
        await users_collection.create_index([("tenant_id", ASCENDING)])
        
        # Leads indexes
        await leads_collection.create_index([("tenant_id", ASCENDING)])
        await leads_collection.create_index([("email", ASCENDING)])
        await leads_collection.create_index([("grade", ASCENDING)])
        await leads_collection.create_index([("status", ASCENDING)])
        await leads_collection.create_index([("created_at", DESCENDING)])
        await leads_collection.create_index([
            ("tenant_id", ASCENDING),
            ("created_at", DESCENDING)
        ])
        
        # Conversations indexes
        await conversations_collection.create_index([("session_id", ASCENDING)], unique=True)
        await conversations_collection.create_index([("tenant_id", ASCENDING)])
        await conversations_collection.create_index([("lead_id", ASCENDING)])
        
        # KB chunks indexes
        await kb_chunks_collection.create_index([("tenant_id", ASCENDING)])
        await kb_chunks_collection.create_index([("document_id", ASCENDING)])
        
        # Events indexes
        await events_collection.create_index([("tenant_id", ASCENDING)])
        await events_collection.create_index([("lead_id", ASCENDING)])
        await events_collection.create_index([("created_at", DESCENDING)])
        
        logger.info("Successfully created database indexes")
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")
        raise


def get_tenants_collection():
    """Get tenants collection (for routes to use)"""
    return tenants_collection

def get_users_collection():
    """Get users collection (for routes to use)"""
    return users_collection

def get_leads_collection():
    """Get leads collection (for routes to use)"""
    return leads_collection

def get_conversations_collection():
    """Get conversations collection (for routes to use)"""
    return conversations_collection

def get_kb_chunks_collection():
    """Get kb_chunks collection (for routes to use)"""
    return kb_chunks_collection

def get_events_collection():
    """Get events collection (for routes to use)"""
    return events_collection


async def init_default_tenant():
    """Initialize default tenant if not exists"""
    try:
        # Check if collections are initialized
        if tenants_collection is None:
            logger.warning("Collections not initialized, skipping default tenant creation")
            return
        
        existing = await tenants_collection.find_one({"tenant_id": settings.default_tenant_id})
        if not existing:
            default_tenant = {
                "tenant_id": settings.default_tenant_id,
                "tenant_key": "demo-key-12345",
                "name": settings.default_tenant_name,
                "email": settings.gmail_address,
                "settings": {
                    "greeting": "Hi! I'm here to help you. What can I assist you with today?",
                    "lead_questions": [
                        "What's your name?",
                        "What's your email address?",
                        "What's your phone number?",
                        "What service are you interested in?",
                        "What's your budget range?",
                        "What's your timeline?"
                    ],
                    "hot_threshold": settings.hot_lead_threshold,
                    "warm_threshold": settings.warm_lead_threshold,
                    "notification_emails": [settings.gmail_address],
                    "brand_color": "#6366f1",
                    "language": "en"
                },
                "active": True
            }
            await tenants_collection.insert_one(default_tenant)
            logger.info(f"Created default tenant: {settings.default_tenant_id}")
    except Exception as e:
        logger.error(f"Failed to initialize default tenant: {e}")
