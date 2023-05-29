import json

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from .auctions import _update_auction, get_auction_update_model, _get_auction

from app.models.price import Price

ws_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>EcoFood Auctions</title>
    </head>
    <body>
        <h1>EcoFood Auctions</h1>
        <form action="" onsubmit="connectWS(event)">
            <span>Auction ID: <input type="text" id="auction-id" autocomplete="off"/></span>
            <span>Shop ID: <input type="text" id="shop-id" autocomplete="off"/></span>
            <button id="confirm">Confirm</button>
        </form>
        <form action="" id="auction-form" onsubmit="sendMessage(event)" style="display:none">
            <span>Message: <input type="text" id="messageText" autocomplete="off"/></span>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws;
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            };
            function connectWS(event) {
                var auction_id = document.getElementById("auction-id").value
                var shop_id = document.getElementById("shop-id").value
                console.log(`Auction ID= ${auction_id}`)
                console.log(`Shop ID= ${shop_id}`)
                ws = new WebSocket(`ws://localhost:2000/ws/auctions/${auction_id}/shops/${shop_id}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                document.getElementById("auction-id").disabled = true;
                document.getElementById("shop-id").disabled = true;
                document.getElementById("confirm").disabled = true;
                document.getElementById("auction-form").style.display = "block";
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: map[str, list[WebSocket]] = {}

    async def connect(self, auction_id: str, websocket: WebSocket):
        await websocket.accept()
        if auction_id not in self.active_connections:
            self.active_connections[auction_id] = []
        self.active_connections[auction_id].append(websocket)

    def disconnect(self, auction_id: str, websocket: WebSocket):
        self.active_connections[auction_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, auction_id: str, message: str):
        for connection in self.active_connections[auction_id]:
            await connection.send_text(message)


manager = ConnectionManager()


@ws_router.get("/")
async def get():
    return HTMLResponse(html)


@ws_router.websocket("/auctions/{auction_id}/shops/{shop_id}")
async def websocket_endpoint(websocket: WebSocket, auction_id: str, shop_id: str):
    await manager.connect(auction_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            price_data = json.loads(data)

            # use pydantic validations
            price = Price(
                amount=float(price_data["amount"]),
                currency=price_data["currency"],
            )

            try:
                auction = _get_auction(auction_id, websocket.app)
                if auction["bid"]:
                    if auction["bid"]["currency"] != price_data["currency"] or float(auction["bid"]["amount"]) >= float(price.amount):
                        await manager.send_personal_message(f"Your bid price must be greater than current bid and "
                                                            f"currency must be equal.", websocket)
                        continue
            except HTTPException:
                await manager.send_personal_message(f"An error occurred while getting current bid. Please try again",
                                                    websocket)

            try:
                auction_update_model = get_auction_update_model(
                    shop_id=shop_id,
                    bid=price,
                )

                auction_update = _update_auction(auction_id, websocket.app, auction_update_model)

                broadcast_message = json.dumps(jsonable_encoder(auction_update))

                await manager.broadcast(auction_id, broadcast_message)
            except HTTPException:
                await manager.send_personal_message(f"An error occurred while updating your bid. Please try again",
                                                    websocket)

    except WebSocketDisconnect:
        manager.disconnect(auction_id, websocket)
        await manager.broadcast(auction_id, f"Shop #{shop_id} left the auction")  # might not be necessary
