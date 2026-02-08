"""MongoDB async connection using Motor"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional
from .config import settings


class DatabaseManager:
    """Singleton MongoDB client manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect(cls):
        """Initialize MongoDB connection"""
        cls.client = AsyncIOMotorClient(settings.mongo_url)
        cls.db = cls.client[settings.mongo_db_name]
        print(f"✅ Connected to MongoDB: {settings.mongo_db_name}")
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            print("✅ Closed MongoDB connection")
    
    @classmethod
    async def create_indexes(cls):
        """Create database indexes for optimal query performance"""
        if cls.db is None:
            raise RuntimeError("Database not initialized")
        
        # Employees collection indexes
        employees = cls.db.employees
        await employees.create_index("employee_id", unique=True)
        await employees.create_index("email", unique=True)
        await employees.create_index("department")
        await employees.create_index([("full_name", "text")])  # Text search
        
        # Attendance collection indexes
        attendance = cls.db.attendance
        await attendance.create_index([("employee_id", 1), ("date", 1)], unique=True)
        await attendance.create_index("date")
        await attendance.create_index("employee_id")
        await attendance.create_index("status")
        
        # Users collection indexes
        users = cls.db.users
        await users.create_index("email", unique=True)
        
        print("✅ Created database indexes")


# Convenience functions to get collections
def get_employees_collection() -> AsyncIOMotorCollection:
    """Get employees collection"""
    if DatabaseManager.db is None:
        raise RuntimeError("Database not initialized")
    return DatabaseManager.db.employees


def get_attendance_collection() -> AsyncIOMotorCollection:
    """Get attendance collection"""
    if DatabaseManager.db is None:
        raise RuntimeError("Database not initialized")
    return DatabaseManager.db.attendance


def get_users_collection() -> AsyncIOMotorCollection:
    """Get users collection"""
    if DatabaseManager.db is None:
        raise RuntimeError("Database not initialized")
    return DatabaseManager.db.users
