from redis_om import JsonModel, Field


class Product(JsonModel):
    name: str = Field(index=True)
    price: int = Field(index=True)
    quantity: int = Field(index=True)
