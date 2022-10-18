import asyncio
import uvicorn
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import Migrator, NotFoundError

import constants
from models import Product

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[constants.FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

Migrator().run()


@app.get("/")
async def root():
    return "I'm alive!"


@app.post("/products")
async def create_product(product: Product, response: Response):
    pk = product.save()
    response.status_code = status.HTTP_201_CREATED
    return Product.get(pk)


@app.get("/products")
async def list_products():
    return await asyncio.gather(*[Product.get(pk) for pk in Product.all_pks()])


@app.get("/products/{pk}")
async def get_product(pk: str):
    try:
        return Product.get(pk)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found") from exc


@app.delete("/products/{pk}")
async def delete_product(pk: str, response: Response):
    Product.delete(pk)
    response.status_code = status.HTTP_204_NO_CONTENT
    return


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=constants.APP_HOST,
        port=constants.APP_PORT,
        reload=constants.APP_ENV == "local",
        reload_dirs=["./src"],
    )
