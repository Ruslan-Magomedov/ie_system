from fastapi import APIRouter

from src.schemas import OperationRequest
from src.services import operations



router = APIRouter()



@router.post("/operations/income")
def add_income(data: OperationRequest):
    return operations.income(data=data)



@router.post("/operations/expense")
def add_expense(data: OperationRequest):
    return operations.expense(data=data)
