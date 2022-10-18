import time
import uvicorn
import requests
from fastapi import FastAPI, Request, Response, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import Migrator, get_redis_connection

from models import Order
import constants
import enums


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[constants.FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

Migrator().run()

queue = get_redis_connection(url=constants.QUEUE_URL, decode_responses=True)


@app.get("/")
async def root():
    return "I'm alive!"


@app.get("/orders/{pk}")
async def get_order(pk: str):
    return Order.get(pk)


@app.post("/orders")
async def create_order(request: Request, response: Response, bg_tasks: BackgroundTasks):
    # body: {"product_id": 123, "quantity": 42}
    body = await request.json()

    req = requests.get(
        constants.INVENTORY_URL + "/products/" + body["product_id"],
        timeout=10,
    )

    # Handle 404

    product = req.json()

    price = product["price"]
    fee = price * 0.2
    total = price + fee

    order = Order(
        product_id=body["product_id"],
        price=price,
        fee=fee,
        total=total,
        quantity=body["quantity"],
        status=enums.Status.PENDING,
    )
    order.save()
    bg_tasks.add_task(complete_order, order)

    response.status_code = status.HTTP_201_CREATED

    return


def complete_order(order: Order):
    time.sleep(5)
    order.status = enums.Status.COMPLETED
    order.save()
    # Add event to Redis Streams queue
    queue.xadd("order_completed", order.dict(), "*")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=constants.APP_HOST,
        port=constants.APP_PORT,
        reload=constants.APP_ENV == "local",
        reload_dirs=["./src"],
    )
