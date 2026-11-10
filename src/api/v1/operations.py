from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependency import get_db
from src.schemas import OperationRequest
from src.services import operations



router = APIRouter()



@router.post("/operations/income")
def add_income(data: OperationRequest, db: Session = Depends(get_db)):
    return operations.income(db, data=data)



@router.post("/operations/expense")
def add_expense(data: OperationRequest, db: Session = Depends(get_db)):
    return operations.expense(db, data=data)
