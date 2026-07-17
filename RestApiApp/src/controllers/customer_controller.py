from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.services import customer_service
from src.models.customer import Customer
from src.security_utils import verify_password
from src.security import create_access_token

router = APIRouter()

# Register new users (Now handles role assignment and password hashing)
@router.post("/register")
async def register(customer: Customer):
    # Call service layer to check if username exists
    existing = await customer_service.get_customer_by_username(customer.username)
    if existing:
        raise HTTPException(status_code=400, detail="Customer already exists")
    
    # We pass the customer model to the service, which handles hashing and role assignment
    return await customer_service.create_customer(customer)

# Login and receive JWT
@router.post("/login")
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
    # 1. Fetch user from database
    user = await customer_service.get_customer_by_username(credentials.username)
    
    # 2. Verify credentials
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )
    
    # 3. Generate token (user['role'] comes from the database)
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    
    return {"access_token": token, "token_type": "bearer"}