from fastapi.exceptions import HTTPException

from src.database import SessionLocal
from src.schemas import OperationRequest
from src.repository import wallets as wallet_rep



def income(data: OperationRequest):
    db = SessionLocal()
    try:
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
    finally:
        db.close()



def expense(data: OperationRequest):
    db = SessionLocal()
    try:
        if not wallet_rep.is_wallet_exist(db, data.wallet_name):
            raise HTTPException(status_code=404, detail=f"Wallet '{data.wallet_name}', not found")

        wallet = wallet_rep.get_wallet_by_name(db, data.wallet_name)
        
        if wallet.balance < data.amount:
            raise HTTPException(status_code=400, detail=f"There not enough funds - balance {wallet.balance}")
        
        wallet = wallet_rep.add_expense(db, data.wallet_name, data.amount)

        db.commit()
        
        return {
            "message": "Expense added",
            "wallet": data.wallet_name,
            "amount": data.amount,
            "description": data.description,
            "balance": wallet.balance
        }
    finally:
        db.close()
