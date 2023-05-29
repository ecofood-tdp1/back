from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.models.transactions import Transaction

transactions_router = APIRouter()


@transactions_router.post(
    "",
    response_description="Create a new transaction",
    status_code=status.HTTP_201_CREATED,
    response_model=Transaction,
)
def create_transaction(request: Request, transaction: Transaction = Body(...)):
    transaction = jsonable_encoder(transaction)
    new_transaction = request.app.database["transactions"].insert_one(transaction)
    created_transaction = request.app.database["transactions"].find_one(
        {"_id": new_transaction.inserted_id}
    )

    return created_transaction


@transactions_router.get(
    "", response_description="List all transactions", response_model=List[Transaction]
)
def get_transactions(request: Request):
    transactions = list(request.app.database["transactions"].find(limit=100))
    return transactions


@transactions_router.get(
    "/{id}", response_description="Get a single transaction by id", response_model=Transaction
)
def find_transaction(id: str, request: Request):
    if (transaction := request.app.database["transactions"].find_one({"_id": id})) is not None:
        return transaction
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with ID {id} not found"
    )
