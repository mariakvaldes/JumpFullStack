from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from src.models.customer import Customer  # Make sure this is imported
from src.services import customer_service # To check or save customers

router = APIRouter()

# Password hashing & JWT configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_super_secret_key_here"  # Match what your app needs
ALGORITHM = "HS256"

class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "customer"  # Can be "customer" or "role_admin"

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserRegister):
    existing = await customer_service.get_customer_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    
    # Create a proper Customer model instance instead of a raw dict
    new_customer = Customer(
        username=user.username,
        password=hashed_password,
        role=user.role
    )
    
    created = await customer_service.create_customer(new_customer)
    return {"message": "User registered successfully", "username": user.username}

@router.post("/login")
async def login(user: UserLogin):
    # Fetch customer from database
    db_user = await customer_service.get_customer_by_username(user.username)
    
    if not db_user or not pwd_context.verify(user.password, db_user.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )
    
    # Generate JWT token
    token_payload = {
        "sub": db_user.get("username"),
        "role": db_user.get("role", "customer")
    }
    access_token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.get("role", "customer")
    }