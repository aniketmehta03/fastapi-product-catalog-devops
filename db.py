import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import MobileApp

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mongodb://devops:devops123@mongo:27017/mobileapp"  # fallback for local
)

client = AsyncIOMotorClient(DATABASE_URL)
database = client.mobileapp

async def init_db():
    await init_beanie(database=database, document_models=[MobileApp])
