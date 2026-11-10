from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependency import get_db
from src.services import wallets as wallet_service
from src.schemas import CreateWalletRequest



router = APIRouter()



@router.get("/balance")
def get_balance(wallet_name: str | None = None, db: Session = Depends(get_db)):
    return wallet_service.get_wallet(db, wallet_name=wallet_name)



@router.post("/wallets")
def crate_wallet(wallet: CreateWalletRequest, db: Session = Depends(get_db)):
    return wallet_service.crate_wallet(db, wallet=wallet)
