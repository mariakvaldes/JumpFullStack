from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from src.services import account_service
from src.models.account import Account

router = APIRouter()

# --- Existing Routes ---
@router.post("/accounts")
async def add_account(account: Account):
    return await account_service.create_account(account)

@router.post("/accounts/{id}/deposit")
async def deposit_money(id: str, request: dict):
    return await account_service.deposit(id, request["amount"])

@router.post("/accounts/{id}/withdraw")
async def withdraw_money(id: str, request: dict):
    return await account_service.withdraw(id, request["amount"])

# --- New: Get All Accounts ---
@router.get("/accounts")
async def get_all_accounts():
    return await account_service.get_all_accounts()

# --- New: Get Account by ID & Balance ---
@router.get("/accounts/{id}")
async def get_account(id: str):
    account = await account_service.get_account_by_id(id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/accounts/{id}/balance")
async def get_balance(id: str):
    account = await account_service.get_account_by_id(id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"balance": account["balance"]}

# --- New: Delete Account ---
@router.delete("/accounts/{id}")
async def close_account(id: str):
    # Logic: check balance first in service layer
    return await account_service.delete_account(id)

# --- Updated: Transactions with Filtering & Sorting ---
@router.get("/accounts/{id}/transactions")
async def get_account_transactions(
    id: str, 
    type: Optional[str] = Query(None), 
    sort: str = Query("desc")
):
    return await account_service.get_transactions(id, type, sort)