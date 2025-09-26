import os
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client: AsyncIOMotorClient | None = None
db = None

async def connect_to_mongo():
    global mongo_client, db
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")

    if not mongo_uri or not db_name:
        print("⚠️ Skipping MongoDB connection: missing MONGO_URI or MONGO_DB_NAME")
        return

    mongo_client = AsyncIOMotorClient(mongo_uri)
    db = mongo_client[db_name]
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("🛑 MongoDB connection closed")
