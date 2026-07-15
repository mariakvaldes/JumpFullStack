from pydantic import BaseModel, Field
from typing import Optional

class Account(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    customer_id: str
    balance: float = 0.0
    account_type: str # e.g., "SAVINGS" or "CHECKING"