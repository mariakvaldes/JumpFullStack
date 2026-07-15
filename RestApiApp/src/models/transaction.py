from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    account_id: str
    type: str  # "DEPOSIT" or "WITHDRAW"
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)