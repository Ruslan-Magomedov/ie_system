from sqlalchemy.orm import Mapped, mapped_column

from decimal import Decimal

from src.database import Base



class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal]
