from sqlalchemy.orm import Session

from decimal import Decimal
from src.models import Wallet



def get_all_wallets(db: Session) -> list[Wallet]:
    return db.query(Wallet).all()



def is_wallet_exist(db: Session, wallet: str) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet).first() is not None



def add_income(db: Session, wallet: str, amount: Decimal) -> Wallet:
    wallet_db = db.query(Wallet).filter(Wallet.name == wallet).first()
    wallet_db.balance += amount
    return wallet_db



def add_expense(db: Session, wallet: str, amount: Decimal) -> Wallet:
    wallet_db = db.query(Wallet).filter(Wallet.name == wallet).first()
    wallet_db.balance -= amount
    return wallet_db



def get_wallet_by_name(db: Session, wallet: str) -> Wallet:
    return db.query(Wallet).filter(Wallet.name == wallet).first()



def create_wallet(db: Session, wallet: str, initial_balance: Decimal) -> Wallet:
    new_wallet = Wallet(name=wallet, balance=initial_balance)
    db.add(new_wallet)
    db.flush()
    return new_wallet
