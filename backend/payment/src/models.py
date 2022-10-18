from redis_om import JsonModel, Field
import enums


class Order(JsonModel):
    product_id: str = Field(index=True)
    price: int
    fee: int
    total: int
    quantity: int
    status: enums.Status = Field(index=True)
