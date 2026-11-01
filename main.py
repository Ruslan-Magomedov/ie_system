from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from pydantic import BaseModel



app = FastAPI()

BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str
    amount: float
    description: str | None = None



@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    # Если имя кошелько не указанно - возвращаем общий баланс
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}
    # Проверяем существует ли запрашиваемый кошелек
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}', not found"
        )
    # Возвращаем баланс конкретного кошелька
    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}



@app.post("/wallets/{name}")
def crate_wallet(name: str, initial_balance: float = 0):
    # Проверяем существует ли такой кошелек
    if name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail=f"wallet '{name}' already exists"
        )
    # Создаем новый кошелек с начальным балансом
    BALANCE[name] = initial_balance
    # Возвращаем информацию о кошельке
    return {
        "message": f"Wallet '{name}' created",
        "wallet": name,
        "balance": BALANCE[name]
    }



@app.post("/operations/income")
def add_income(data: OperationRequest):
    # Проверяем существует ли запрашиваемый кошелек
    if data.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{data.wallet_name}', not found"
        )
    # Проверяем что сумма положительная
    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amoun must be positive"
        )
    # Добавляем доход к балансу кошелька
    BALANCE[data.wallet_name] += data.amount
    # Возвращаем информацию о кошельке
    return {
        "message": "Income added",
        "wallet": data.wallet_name,
        "amount": data.amount,
        "description": data.description,
        "balance": BALANCE[data.wallet_name]
    }



@app.post("/operations/expense")
def add_expense(data: OperationRequest):
    # Проверяем существует ли запрашиваемый кошелек
    if data.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{data.wallet_name}', not found"
        )
    # Проверяем что сумма положительная
    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amoun must be positive"
        )
    # Проверяем достаточно ли средств в кошельке
    if BALANCE[data.wallet_name] < data.amount:
        raise HTTPException(
            status_code=400,
            detail=f"There not enough funds - balance {BALANCE[data.wallet_name]}"
        )
    # Вычитаем расход из баланса кошелька
    BALANCE[data.wallet_name] -= data.amount
    # Возврощаем информацию о кошельке
    return {
        "message": "Expense added",
        "wallet": data.wallet_name,
        "amount": data.amount,
        "description": data.description,
        "balance": BALANCE[data.wallet_name]
    }