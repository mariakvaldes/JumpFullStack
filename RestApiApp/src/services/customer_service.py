from src.repos.repository import customer_collection
from src.models.customer import Customer
from bson import ObjectId

async def create_customer(customer: Customer):
    # Logic: Convert model to dict and insert into MongoDB
    customer_dict = customer.model_dump(by_alias=True)
    result = await customer_collection.insert_one(customer_dict)
    return {"id": str(result.inserted_id), "username": customer.username}

async def get_customer_by_username(username: str):
    return await customer_collection.find_one({"username": username})