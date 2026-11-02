from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from pydantic import BaseModel, Field, field_validator



app = FastAPI()

BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=120)
    amount: float
    description: str | None = Field(None, max_length=255)

    @field_validator("amount")
    def amount_must_be_positive(cls, value: float) -> float:
        """
        валидатор для проверки что сумма положительная
        - проверяем что число положительное и возвращаем
        - иначе выбрасываем ошибку ValueError
        """
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value

    @field_validator("wallet_name")
    def wallet_name_validator(cls, value: str) -> str:
        """
        валидатор для проверки имени кошелька
        - удаляем пробелы вначале и в конце строки
        - если строка пустая выбрасываем ошибку ValueError
        - иначе возврощаем результат
        """
        value = value.strip()
        if not value:
            raise ValueError("Wallet name can't be empty")
        return value



class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=120)
    initial_balance: float = 0

    @field_validator("initial_balance")
    def balance_not_negative(cls, value: float) -> float:
        """
        валидатор для проверки что сумма положительная
        - проверяем что число положительное и возвращаем
        """
        if value < 0:
            raise ValueError("Balance can't be negative")
        return value

    @field_validator("name")
    def name_validator(cls, value: str) -> str:
        """
        валидатор для проверки имени кошелька
        - удаляем пробелы вначале и в конце строки
        - если строка пустая выбрасываем ошибку ValueError
        - иначе возврощаем результат
        """
        value = value.strip()
        if not value:
            raise ValueError("Name can't be empty")
        return value 



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



@app.post("/wallets")
def crate_wallet(wallet: CreateWalletRequest):
    # Проверяем существует ли такой кошелек
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail=f"wallet '{wallet.name}' already exists"
        )
    # Создаем новый кошелек с начальным балансом
    BALANCE[wallet.name] = wallet.initial_balance
    # Возвращаем информацию о кошельке
    return {
        "message": f"Wallet '{wallet.name}' created",
        "wallet": wallet.name,
        "balance": BALANCE[wallet.name]
    }



@app.post("/operations/income")
def add_income(data: OperationRequest):
    # Проверяем существует ли запрашиваемый кошелек
    if data.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{data.wallet_name}', not found"
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