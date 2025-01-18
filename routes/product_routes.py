from fastapi import APIRouter, Depends
from models.dbsession import get_db
from sqlalchemy.orm import Session
from utility.jwt import verify_token
from models.users import User

router = APIRouter()

@router.get("/products")
async def list_products(auth_user: User = Depends(verify_token), db:Session=Depends(get_db)):
    return {"message": "List of products"}


@router.get("/product/{product_id}")
async def get_product(product_id: int):
    return {"message": "Product details"}


@router.post("/product/{product_id}")
async def create_product(product_id: int):
    return {"message": "Product created successfully " + str(product_id)}


@router.put("/product/{product_id}")
async def update_product(product_id: int):
    return {"message": "Product updated successfully"}


@router.delete("/product/{product_id}")
async def delete_product(product_id: int):
    return {"message": "Product deleted successfully"}
