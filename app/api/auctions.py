from typing import List, Optional

from fastapi import APIRouter, Request, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from starlette.requests import HTTPConnection

from app.models.auctions import Auction, AuctionUpdate, AuctionStatus
from app.models.price import Price

auctions_router = APIRouter()


@auctions_router.post(
    "",
    response_description="Create a new auction",
    status_code=status.HTTP_201_CREATED,
    response_model=Auction,
)
def create_auction(request: Request, auction: Auction = Body(...)):
    auction = jsonable_encoder(auction)
    new_auction = request.app.database["auctions"].insert_one(auction)
    created_auction = request.app.database["auctions"].find_one(
        {"_id": new_auction.inserted_id}
    )

    return created_auction


@auctions_router.get(
    "/", response_description="List all auctions", response_model=List[Auction]
)
def get_auctions(request: Request):
    auctions = list(request.app.database["auctions"].find(limit=100))
    return auctions


@auctions_router.get(
    "/{auction_id}", response_description="Get a single auction by id", response_model=Auction
)
def get_auction(auction_id: str, request: Request):
    return _get_auction(auction_id, request.app)


def _get_auction(auction_id: str, app: HTTPConnection):
    if (auction := app.database["auctions"].find_one({"_id": auction_id})) is not None:
        return auction
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Auction with ID {auction_id} not found"
    )


@auctions_router.put(
    "/{auction_id}", response_description="Update an auction", response_model=Auction
)
def update_auction(auction_id: str, request: Request, auction: AuctionUpdate = Body(...)):
    return _update_auction(auction_id, request.app, auction)


def _update_auction(auction_id: str, app: HTTPConnection, auction: AuctionUpdate = Body(...)):
    auction = {k: v for k, v in auction.dict().items() if v is not None}
    if len(auction) >= 1:
        update_result = app.database["auctions"].update_one(
            {"_id": auction_id}, {"$set": jsonable_encoder(auction)}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Auction with ID {auction_id} not found",
            )

    if (
            existing_auction := app.database["auctions"].find_one({"_id": auction_id})
    ) is not None:
        return existing_auction

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Auction with ID {id} not found"
    )


def get_auction_update_model(
        auction_status: Optional[AuctionStatus] = None,
        bid: Optional[Price] = None,
        shop_id: Optional[str] = None,
):
    update_model = AuctionUpdate()

    if auction_status:
        update_model.status = auction_status

    if bid:
        update_model.bid = bid

    if shop_id:
        update_model.current_winner_id = shop_id

    return update_model
