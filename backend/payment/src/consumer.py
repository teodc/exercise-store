import time
from redis_om import get_redis_connection

from models import Order
from constants import QUEUE_URL, EVENT_GROUP, EVENT_KEY
from enums import Status

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
                obj = event[1][0][1]
                order = Order.get(obj["pk"])
                order.status = Status.REFUNDED
                order.save()
    except Exception as e:
        print(str(e))

    time.sleep(1)
