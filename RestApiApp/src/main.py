from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import jwt

from src.controllers import account_controller, customer_controller, auth_controller

app = FastAPI(title="Bank REST API", version="1.0.0")

# --- Enable CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # React Vite dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers (Authorization, Content-Type, etc.)
)

# --- Include Routers ---
app.include_router(auth_controller.router)       
app.include_router(customer_controller.router)   
app.include_router(account_controller.router)    

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bank REST API"}