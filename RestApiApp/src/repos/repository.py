from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = "mongodb+srv://mariavaldes003_db_user:JQAuhLVWzOATZADr@cluster.5zvq2jl.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.bank_db
customer_collection = database.get_collection("customers")
account_collection = database.get_collection("accounts")