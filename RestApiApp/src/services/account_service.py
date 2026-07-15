from src.repos.repository import account_collection
from src.models.account import Account

async def create_account(account: Account):
    # Exclude the id here as well so MongoDB generates a fresh one
    account_dict = account.model_dump(by_alias=True, exclude={"id"})
    result = await account_collection.insert_one(account_dict)
    return {"id": str(result.inserted_id), **account_dict}