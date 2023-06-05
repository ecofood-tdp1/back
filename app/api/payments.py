from app.models.mocks import MockedCard
from app.models.price import Price, Currency
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
import logging

from app.models.payments import PaymentTransaction, TransactionBody, PaymentType

logger = logging.getLogger('app')
payments_router = APIRouter()


@payments_router.post(
    "",
    response_description="Create a new payment",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentTransaction,
)
def create_payment_transaction(request: Request, payment: TransactionBody = Body(...)):
    payment = jsonable_encoder(payment)

    user = request.app.database["users"].find_one({"_id": payment["user_id"]})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id"
        )

    pm = payment["payment_method"]

    decoded_pan = pm["pan"]
    decoded_cardholder_name = pm["cardholder_name"]
    decoded_expiration_date = pm["expiration_date"]
    decoded_issuer = pm["issuer"]

    decoded_card = MockedCard(
        pan=decoded_pan,
        cardholder_name=decoded_cardholder_name,
        expiration_date=decoded_expiration_date,
        issuer=decoded_issuer,
    )

    payment_method = request.app.database["mocked_cards"].find_one({"pan": decoded_pan})

    if not payment_method:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=f"Payment Method with PAN {pm['pan']} not valid"
        )

    if MockedCard(**payment_method) != decoded_card:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=f"Payment Method with PAN {pm['pan']} does not "
                                                                 f"match card data"
        )

    payment_transaction = PaymentTransaction(
        type=PaymentType.card,
        user_id=payment["user_id"],
        last_numbers=decoded_card.pan[-4:],
        issuer=decoded_issuer,
        total=Price(
            amount=payment["total"]["amount"],
            currency=payment["total"]["currency"],
        )
    )

    new_payment = request.app.database["payments"].insert_one(jsonable_encoder(payment_transaction))
    created_payment = request.app.database["payments"].find_one({"_id": new_payment.inserted_id})

    if not created_payment:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Payment transaction failed"
        )

    return created_payment


@payments_router.get(
    "",
    response_description="List all payment transactions",
    response_model=List[PaymentTransaction])
def list_payment_transactions(request: Request, user_id: Optional[str] = None):
    filters = {}
    if user_id:
        filters["user_id"] = user_id

    cards = list(request.app.database["payments"].find(filters, limit=100))
    return cards
