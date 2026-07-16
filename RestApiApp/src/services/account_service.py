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

async def withdraw(account_id: str, amount: float):
    # 1. Fetch current account state
    account = await account_collection.find_one({"_id": ObjectId(account_id)})
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # 2. Cannot withdraw more than balance
    if account["balance"] < amount:
        raise HTTPException(status_code=400, detail="Cannot withdraw more than balance")
    
    # 3. Update balance
    result = await account_collection.find_one_and_update(
        {"_id": ObjectId(account_id)},
        {"$inc": {"balance": -amount}},
        return_document=True
    )
    
    # 4. Maintain transaction record
    await transaction_collection.insert_one({
        "account_id": account_id,
        "type": "WITHDRAW",
        "amount": amount,
        "timestamp": datetime.utcnow()
    })
    
    return {"message": "Withdrawal successful", "new_balance": result["balance"]}

async def get_all_accounts():
    accounts = await account_collection.find().to_list(100)
    for a in accounts:
        a["_id"] = str(a["_id"])
    return accounts

async def get_account_by_id(account_id: str):
    account = await account_collection.find_one({"_id": ObjectId(account_id)})
    if account:
        account["_id"] = str(account["_id"])
    return account

async def delete_account(account_id: str):
    account = await get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account["balance"] != 0:
        raise HTTPException(status_code=400, detail="Cannot close: Balance must be 0")
    
    await account_collection.delete_one({"_id": ObjectId(account_id)})
    return {"message": "Account successfully deleted"}

async def get_transactions(account_id: str, type: str = None, sort: str = "desc"):
    query = {"account_id": account_id}
    if type:
        query["type"] = type
        
    order = -1 if sort == "desc" else 1
    
    cursor = transaction_collection.find(query).sort("timestamp", order)
    transactions = await cursor.to_list(length=100)
    
    for t in transactions:
        t["_id"] = str(t["_id"])
        if "timestamp" in t:
            t["timestamp"] = t["timestamp"].isoformat()
    return transactions