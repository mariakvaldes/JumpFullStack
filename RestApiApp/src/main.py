from fastapi import FastAPI
from src.controllers.customer_controller import router as customer_router

app = FastAPI()

# Include the router so your app knows about the /customers endpoint
app.include_router(customer_router)

@app.get("/")
async def root():
    return {"message": "Bank API is running!"}