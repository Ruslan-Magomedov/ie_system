from fastapi import FastAPI
from uvicorn import run

from src.api.v1.wallets import router as wallet_router
from src.api.v1.operations import router as operation_router

from src.database import Base, engin



app = FastAPI()
app.include_router(wallet_router, prefix="/api/v1", tags=["Wallet"])
app.include_router(operation_router, prefix="/api/v1", tags=["Operations"])



Base.metadata.create_all(bind=engin)



if __name__ == "__main__":
    run("main:app", reload=True)
