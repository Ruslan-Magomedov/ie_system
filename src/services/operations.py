from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.schemas import OperationRequest
from src.repository import wallets as wallet_rep



def income(db: Session, data: OperationRequest):
    if not wallet_rep.is_wallet_exist(db, data.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{data.wallet_name}', not found")
    
    wallet = wallet_rep.add_income(db, data.wallet_name, data.amount)

    db.commit()

    return {
        "message": "Income added",
        "wallet": data.wallet_name,
        "amount": data.amount,
        "description": data.description,
        "balance": wallet.balance
    }



def expense(db: Session, data: OperationRequest):
    if not wallet_rep.is_wallet_exist(db, data.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{data.wallet_name}', not found")

    wallet = wallet_rep.get_wallet_by_name(db, data.wallet_name)
    
    if wallet.balance < data.amount:
        raise HTTPException(status_code=400, detail=f"There not enough funds - balance {wallet.balance:g}")
    
    wallet = wallet_rep.add_expense(db, data.wallet_name, data.amount)

    db.commit()
    
    return {
        "message": "Expense added",
        "wallet": data.wallet_name,
        "amount": data.amount,
        "description": data.description,
        "balance": wallet.balance
    }
