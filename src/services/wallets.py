from fastapi.exceptions import HTTPException

from src.schemas import CreateWalletRequest
from src.repository import wallets as wallet_rep
from src.schemas import CreateWalletRequest



def get_wallet(wallet_name: str | None = None):
    if wallet_name is None:
        wallet = wallet_rep.get_all_wallets()
        return {"total_balance": sum(wallet.values())}
    
    if not wallet_rep.is_wallet_exist(wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}', not found")

    return {"wallet": wallet_name, "balance": wallet_rep.get_wallet_balance_by_name(wallet_name)}



def crate_wallet(wallet: CreateWalletRequest):
    if wallet_rep.is_wallet_exist(wallet.name):
        raise HTTPException(status_code=400, detail=f"wallet '{wallet.name}' already exists")

    new_balance = wallet_rep.create_wallet(wallet.name, wallet.initial_balance)

    return {
        "message": f"Wallet '{wallet.name}' created",
        "wallet": wallet.name,
        "balance": new_balance
    }
