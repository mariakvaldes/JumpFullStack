from fastapi import FastAPI
from src.controllers.customer_controller import router as customer_router
from src.controllers.account_controller import router as account_router


app = FastAPI()

# /customers endpoint, /account endpoint
app.include_router(customer_router)
app.include_router(account_router)

@app.get("/")
async def root():
    return {"message": "Bank API is running!"}