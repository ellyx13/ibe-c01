import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

class BaseCRUD:
    def __init__(self, database_url: str, database_name: str, collection_name: str):
        self.database_url = database_url
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = self.connect()
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        
    def connect(self):
        return AsyncIOMotorClient(self.database_url)
    
    async def save(self, document: dict) -> str:
        result = await self.collection.insert_one(document)
        return str(result.inserted_id)
    
    async def update_by_id(self, _id, new_data) -> bool:
        query = {"_id": ObjectId(_id)}
        result = await self.collection.update_one(query, {"$set": new_data})
        return result.modified_count > 0
    
    async def delete_by_id(self, _id) -> bool:
        query = {"_id": ObjectId(_id)}
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0
    
    async def get_by_id(self, _id) -> dict:
        query = {"_id": ObjectId(_id)}
        document = await self.collection.find_one(query)
        return document
    
    async def get_by_field(self, field, value) -> list:
        query = {field: value}
        return await self.get_by_query(query)
    
    async def get_by_query(self, query) -> list:
        documents = self.collection.find(query)
        results = []
        async for document in documents:
            document["_id"] = str(document["_id"])
            results.append(document)
        return results