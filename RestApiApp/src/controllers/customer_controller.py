from fastapi import APIRouter, HTTPException
from src.services import customer_service
from src.models.customer import Customer

router = APIRouter()

@router.post("/customers")
async def add_customer(customer: Customer):
    # Call the service layer to handle logic
    existing = await customer_service.get_customer_by_username(customer.username)
    if existing:
        raise HTTPException(status_code=400, detail="Customer already exists")
    
    return await customer_service.create_customer(customer)