from pydantic import BaseModel, Field
from typing import Optional

class Customer(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    username: str
    password: str