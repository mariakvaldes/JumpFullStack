from fastapi import APIRouter
from src.services import account_service
from src.models.account import Account

router = APIRouter()

@router.post("/accounts")
async def add_account(account: Account):
    return await account_service.create_account(account)