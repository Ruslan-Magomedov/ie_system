from fastapi.exceptions import HTTPException

from src.schemas import OperationRequest
from src.repository import wallets as wallet_rep



def income(data: OperationRequest):
    if not wallet_rep.is_wallet_exist(data.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{data.wallet_name}', not found")
    
    new_balance = wallet_rep.add_income(data.wallet_name, data.amount)

    return {
        "message": "Income added",
        "wallet": data.wallet_name,
        "amount": data.amount,
        "description": data.description,
        "balance": new_balance
    }



def expense(data: OperationRequest):
    if not wallet_rep.is_wallet_exist(data.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{data.wallet_name}', not found")

    balance = wallet_rep.get_wallet_balance_by_name(data.wallet_name)
    
    if balance < data.amount:
        raise HTTPException(status_code=400, detail=f"There not enough funds - balance {balance}")
    
    new_balance = wallet_rep.add_expense(data.wallet_name, data.amount)

    return {
        "message": "Expense added",
        "wallet": data.wallet_name,
        "amount": data.amount,
        "description": data.description,
        "balance": new_balance
    }
