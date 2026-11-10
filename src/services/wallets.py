from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.schemas import CreateWalletRequest
from src.repository import wallets as wallet_rep
from src.schemas import CreateWalletRequest



def get_wallet(db: Session, wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallet_rep.get_all_wallets(db)
        return {"total_balance": sum([w.balance for w in wallets])}
    
    if not wallet_rep.is_wallet_exist(db, wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}', not found")

    wallet = wallet_rep.get_wallet_by_name(db, wallet_name)

    return {"wallet": wallet.name, "balance": wallet.balance}



def crate_wallet(db: Session, wallet: CreateWalletRequest):
    if wallet_rep.is_wallet_exist(db, wallet.name):
        raise HTTPException(status_code=400, detail=f"wallet '{wallet.name}' already exists")

    new_wallet = wallet_rep.create_wallet(db, wallet.name, wallet.initial_balance)

    db.commit()
    
    return {
        "message": f"Wallet '{wallet.name}' created",
        "wallet": wallet.name,
        "balance": new_wallet.balance
    }
