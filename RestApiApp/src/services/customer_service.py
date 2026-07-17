from src.repos.repository import customer_collection
from src.models.customer import Customer
from src.security_utils import get_password_hash

async def create_customer(customer: Customer):
    # 1. Convert Pydantic model to dict, excluding the ID if it's None
    customer_dict = customer.model_dump(by_alias=True, exclude={"id"})
    
    # 2. Hash the password
    customer_dict["password"] = get_password_hash(customer_dict["password"])
    
    # 3. Check if any users exist to assign role
    user_count = await customer_collection.count_documents({})
    customer_dict["role"] = "role_admin" if user_count == 0 else "role_customer"
    
    # 4. Save to DB
    result = await customer_collection.insert_one(customer_dict)
    
    return {
        "id": str(result.inserted_id), 
        "username": customer_dict["username"], 
        "role": customer_dict["role"]
    }

async def get_customer_by_username(username: str):
    return await customer_collection.find_one({"username": username})