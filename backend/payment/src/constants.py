import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.environ.get("APP_ENV")
APP_HOST = os.environ.get("APP_HOST")
APP_PORT = int(os.environ.get("APP_PORT"))

QUEUE_URL = os.environ.get("QUEUE_URL")
INVENTORY_URL = os.environ.get("INVENTORY_URL")
FRONTEND_URL = os.environ.get("FRONTEND_URL")

EVENT_GROUP = "payment-group"
EVENT_KEY = "order_refunded"
