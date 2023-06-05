from typing import Optional, List

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
import re
import random
import logging

from app.models.mocks import MockedCard, MockedCardRequestBody

logger = logging.getLogger('app')
mocks_router = APIRouter()


@mocks_router.post(
    "/payment_methods",
    response_description="Create a new payment method",
    status_code=status.HTTP_201_CREATED,
    response_model=MockedCard,
)
def create_mocked_payment_method(request: Request, payment_method: MockedCardRequestBody = Body(...)):
    payment_method = jsonable_encoder(payment_method)
    mocked_card = MockedCard(
        pan=luhn_algorithm(payment_method['issuer']),
        issuer=str(payment_method['issuer']),
        expiration_date=payment_method['expiration_date'],
        cardholder_name=payment_method['cardholder_name'],
    )
    new_card = request.app.database["mocked_cards"].insert_one(jsonable_encoder(mocked_card))
    created_card = request.app.database["mocked_cards"].find_one({"_id": new_card.inserted_id})

    if not created_card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Mocked Card creation failed"
        )

    return created_card


@mocks_router.get(
    "/payment_methods",
    response_description="List all mocked payment methods",
    response_model=List[MockedCard])
def list_payment_methods(request: Request, issuer: Optional[str] = None, cardholder_name: Optional[str] = None):
    filters = {}
    if issuer:
        filters["issuer"] = re.compile(issuer, re.IGNORECASE)

    if cardholder_name:
        filters["cardholder_name"] = re.compile(cardholder_name, re.IGNORECASE)

    cards = list(request.app.database["mocked_cards"].find(filters, limit=100))
    return cards


def make_random_number(number_of_element):
    random_numbers = []
    for i in range(number_of_element):
        random_numbers.append(random.randint(0, 9))
    return random_numbers


def luhn_algorithm(issuer: str):
    if issuer == 'master':
        random_int = make_random_number(13)
        random_int.insert(0, 5)
        random_int.insert(1, 4)
    else:
        random_int = make_random_number(14)
        random_int.insert(0, 4)

    sum_even = []
    sum_odd = []
    for index, element in enumerate(random_int):
        if index % 2 != 0:
            r = random_int[index] * 2
            character_string = list(str(r))
            character_int = map(int, character_string)
            sum_even.append(sum(character_int))
        if index % 2 == 0:
            sum_odd.append(element)
    total_sum = sum(sum_even)+sum(sum_odd) * 9
    random_int.append(total_sum % 10)
    credit_card_number = ''.join(map(str, random_int))
    return credit_card_number
