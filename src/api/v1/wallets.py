from fastapi import APIRouter

from services import wallets as wallet_service
from schemas import CreateWalletRequest



router = APIRouter()



@router.get("/balance")
def get_balance(wallet_name: str | None = None):
    return wallet_service.get_wallet(wallet_name=wallet_name)



@router.post("/wallets")
def crate_wallet(wallet: CreateWalletRequest):
    return wallet_service.crate_wallet(wallet=wallet)
