import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def connect_mongo(database_url):
  # Replace the placeholder with your Atlas connection string
  # Set the Stable API version when creating a new client
  client = AsyncIOMotorClient(database_url)
  # Send a ping to confirm a successful connection
  try:
      await client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
      return client
  except Exception as e:
      print(e)
      
async def do_insert(collection, document):
    result = await collection.insert_one(document)
    print(type(result.inserted_id))
    return str(result.inserted_id)

async def do_insert_many(collection, documents):
    results = await collection.insert_many(documents)
    ids = []
    for id in results.inserted_ids:
        ids.append(str(id))
    return ids

async def count_by_query(collection, query):
    count = await collection.count_documents(query)
    return count

async def get_by_query(collection, query):
    documents = collection.find(query)
    results = []
    async for document in documents:
        document["_id"] = str(document["_id"])
        results.append(document)
    return results

async def update_by_query(collection, query, new_data):
    result = await collection.update_many(query, {"$set": new_data})
    return result.modified_count

async def update_by_id(collection, id, new_data):
    query = {"_id": ObjectId(id)}
    print(query)
    return await update_by_query(collection, query, new_data)

async def delete_by_id(collection, id) -> int:
    query = {"_id": ObjectId(id)}
    result = await collection.delete_one(query)
    return result.deleted_count
      
async def main():
    database_url = "mongodb://localhost:27030/"
    client = await connect_mongo(database_url)
    db = client["app"]
    collection = db["users"]
    document = {"name": "John Doe", "age": 50}
    document_id = await do_insert(collection, document)
    print(f"Inserted document with ID: {document_id}")
    
    result = await delete_by_id(collection, document_id)
    print(f"Delete documents: {result}")
    
    # results = await update_by_id(collection, document_id, {"age": 51})
    # print(f"Updated documents: {results}")
    

    # documents = [{"name": "John Doe", "age": 30}, {"name": "Jane Doe", "age": 25}]
    # result = await do_insert_many(collection, documents)
    # print(f"Inserted document with ID: {result}")
    
    # query = {"age": 25}
    # new_data = {"age": 26}
    # results = await update_by_query(collection, query, new_data)
    # print(f"Found documents: {results}")

asyncio.run(main())