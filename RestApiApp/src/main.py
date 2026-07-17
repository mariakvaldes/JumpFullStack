from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.customer_controller import router as customer_router
from src.controllers.account_controller import router as account_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router) # This now contains /register and /login
app.include_router(account_router)

