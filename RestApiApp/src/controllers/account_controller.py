from fastapi import APIRouter
from src.services import account_service
from src.models.account import Account

router = APIRouter()

@router.post("/accounts")
async def add_account(account: Account):
    return await account_service.create_account(account)

@router.post("/accounts/{id}/deposit")
async def deposit_money(id: str, request: dict):
    # request will look like {"amount": 500}
    return await account_service.deposit(id, request["amount"])