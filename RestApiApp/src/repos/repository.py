from motor.motor_asyncio import AsyncIOMotorClient
import os
from bson import ObjectId

MONGO_DETAILS = "mongodb+srv://mariavaldes003_db_user:JQAuhLVWzOATZADr@cluster.5zvq2jl.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.bank_db

customer_collection = database.get_collection("customers")
account_collection = database.get_collection("accounts")
transaction_collection = database.get_collection("transactions") # transactions to withdraw and deposit

async def get_all_customers():
    return await customer_collection.find().to_list(100)

async def get_all_accounts():
    return await account_collection.find().to_list(100)

async def get_account_by_id(account_id: str):
    return await account_collection.find_one({"_id": ObjectId(account_id)})

async def get_accounts_by_customer(customer_id: str):
    return await account_collection.find({"customer_id": customer_id}).to_list(100)

async def delete_account(account_id: str):
    return await account_collection.delete_one({"_id": ObjectId(account_id)})