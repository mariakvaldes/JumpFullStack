from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "super-secret-key"

# Public endpoint
@app.get("/")
async def public():
    return {"message": "Hello World - Public"}

# Admin endpoint
@app.get("/admin")
async def admin(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access Forbidden")
    return {"message": "Welcome, Admin!"}

# Token generation (The Mock Login)
@app.post("/login")
async def login():
    # In a real app, verify user credentials here
    token = jwt.encode({"sub": "maria", "role": "admin"}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}