from pydantic import BaseModel, Field, field_validator

from decimal import Decimal



class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=120)
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    @field_validator("amount")
    def amount_must_be_positive(cls, value: Decimal) -> Decimal:
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
    initial_balance: Decimal = 0

    @field_validator("initial_balance")
    def balance_not_negative(cls, value: Decimal) -> Decimal:
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