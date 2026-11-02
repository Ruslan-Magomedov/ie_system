BALANCE = {}



def is_wallet_exist(wallet: str) -> bool:
    """TODO реализовать выброс HTTPException в репозитории"""
    return wallet in BALANCE



def add_income(wallet: str, amount: float) -> float:
    BALANCE[wallet] += amount
    return BALANCE[wallet]



def add_expense(wallet: str, amount: float) -> float:
    BALANCE[wallet] -= amount
    return BALANCE[wallet]



def get_wallet_balance_by_name(wallet: str) -> float:
    return BALANCE[wallet]
