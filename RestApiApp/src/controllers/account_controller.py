from fastapi import APIRouter
from src.services import account_service
from src.models.account import Account

router = APIRouter()

@router.post("/accounts")
async def add_account(account: Account):
    return await account_service.create_account(account)

@router.post("/accounts/{id}/deposit")
async def deposit_money(id: str, request: dict):
    return await account_service.deposit(id, request["amount"])

@router.post("/accounts/{id}/withdraw")
async def withdraw_money(id: str, request: dict):
    return await account_service.withdraw(id, request["amount"])