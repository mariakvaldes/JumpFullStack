from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime

# You definitely need this import
from src.models.account import Account 

# And these imports for the database
from src.repos.repository import account_collection, transaction_collection

async def create_account(account: Account):
    # 1. Convert to dictionary
    account_dict = account.model_dump(by_alias=True, exclude={"id"})
    
    # 2. Insert into the database
    result = await account_collection.insert_one(account_dict)
    
    # 3. Add ID back as string
    account_dict["_id"] = str(result.inserted_id)
    
    return account_dict

async def deposit(account_id: str, amount: float):
    # 1. Deposit must be positive
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")
    
    # 2. Update balance in Accounts collection
    result = await account_collection.find_one_and_update(
        {"_id": ObjectId(account_id)},
        {"$inc": {"balance": amount}},
        return_document=True # This returns the updated document
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")

    # 3. Maintain transaction record
    transaction_data = {
        "account_id": account_id,
        "type": "DEPOSIT",
        "amount": amount,
        "timestamp": datetime.utcnow()
    }
    await transaction_collection.insert_one(transaction_data)
    
    return {"message": "Deposit successful", "new_balance": result["balance"]}