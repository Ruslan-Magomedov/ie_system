from fastapi import FastAPI

from src.api.v1.wallets import router as wallet_router
from src.api.v1.operations import router as operation_router



app = FastAPI()
app.include_router(wallet_router, prefix="/api/v1 " tags=["Wallet"])
app.include_router(operation_router, prefix="/api/v1 " tags=["Operations"])
