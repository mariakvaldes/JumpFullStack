from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional
from bson.errors import InvalidId
from src.services import account_service
from src.models.account import Account
# Import your new security dependency
from src.security import get_current_user 
from src.security import create_access_token

router = APIRouter()

# --- Existing Routes (Public) ---
@router.post("/accounts")
async def add_account(account: Account):
    return await account_service.create_account(account)

@router.post("/accounts/{id}/deposit")
async def deposit_money(id: str, request: dict):
    return await account_service.deposit(id, request["amount"])

@router.post("/accounts/{id}/withdraw")
async def withdraw_money(id: str, request: dict):
    return await account_service.withdraw(id, request["amount"])

@router.get("/accounts")
async def get_all_accounts():
    return await account_service.get_all_accounts()

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

# new route for logging in TODO: verify user against database
@router.post("/login")
async def login(request: dict):
    # IN REAL LIFE: Verify user against your database!
    # For now, we simulate finding the user "maria" with "role_admin"
    username = request.get("username")
    password = request.get("password")
    
    if username == "maria" and password == "password123":
        # Create token
        token = create_access_token({"sub": username, "role": "role_admin"})
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

# --- PROTECTED ROUTE: Delete Account (Admin Only) ---
@router.delete("/accounts/{id}")
async def close_account(id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "role_admin":
        raise HTTPException(status_code=403, detail="Access Forbidden")
    
    try:
        return await account_service.delete_account(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Account ID format")

# --- Transactions ---
@router.get("/accounts/{id}/transactions")
async def get_account_transactions(
    id: str, 
    type: Optional[str] = Query(None), 
    sort: str = Query("desc")
):
    return await account_service.get_account_transactions(id, type, sort)