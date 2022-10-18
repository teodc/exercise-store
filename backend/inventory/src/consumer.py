import time
from redis_om import get_redis_connection

from models import Product
from constants import QUEUE_URL, EVENT_GROUP, EVENT_KEY

queue = get_redis_connection(url=QUEUE_URL, decodeResponse=True)

try:
    queue.xgroup_create(EVENT_KEY, EVENT_GROUP)
except:
    print("Group already exists!")

while True:
    try:
        events = queue.xreadgroup(EVENT_GROUP, EVENT_KEY, {EVENT_KEY: ">"}, None)
        if events != []:
            print(events)
            for event in events:
                order = event[1][0][1]
                try:
                    product = Product.get(order["product_id"])
                    product.quantity = product.quantity - int(order["quantity"])
                    product.save()
                except:
                    queue.xadd("refund_order", order, "*")
    except Exception as e:
        print(str(e))

    time.sleep(1)
