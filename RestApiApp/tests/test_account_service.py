import pytest
from unittest.mock import AsyncMock, patch
from src.services.account_service import deposit, withdraw

# Use a valid 24-character hex string
VALID_ID = "507f1f77bcf86cd799439011"

@pytest.mark.asyncio
@patch("src.services.account_service.account_collection", new_callable=AsyncMock)
@patch("src.services.account_service.transaction_collection", new_callable=AsyncMock)
async def test_deposit_success(mock_trans, mock_coll):
    mock_coll.find_one_and_update.return_value = {"balance": 500}
    
    result = await deposit(VALID_ID, 500.0)
    
    assert result["message"] == "Deposit successful"
    assert result["new_balance"] == 500
    mock_coll.find_one_and_update.assert_called_once()

@pytest.mark.asyncio
@patch("src.services.account_service.account_collection", new_callable=AsyncMock)
@patch("src.services.account_service.transaction_collection", new_callable=AsyncMock)
async def test_withdraw_insufficient_funds(mock_trans, mock_coll):
    # Mock finding an account with $50
    mock_coll.find_one.return_value = {"balance": 50}
    
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        await withdraw(VALID_ID, 100.0)
    
    assert exc.value.status_code == 400
    assert "Cannot withdraw more than balance" in exc.value.detail