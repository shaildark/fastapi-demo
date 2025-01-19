from fastapi import APIRouter, Depends
from models.dbsession import get_db
from sqlalchemy.orm import Session, joinedload
from utility.jwt import verify_token
from models.users import User
from models.product import Product
from models.category import Category
from requests.product.list_product import ListProductRequest
from requests.product.product_request import ProductRequest
from utility.response import api_response
from utility.pagination import generate_pagination
from sqlalchemy import func


router = APIRouter(
    prefix="/products",
)

@router.post("/list")
async def list_products(request: ListProductRequest, db:Session=Depends(get_db)):
    query = Product.query(db).options(joinedload(Product.category))

    if request.search:
        query = query.filter(Product.vName.ilike(f"%{request.search}%"))

    if request.category_id:
        query = query.filter(Product.iCategoryId == request.category_id)

    total_items = query.count()
    products = query.offset((request.page - 1) * request.items_per_page).limit(request.items_per_page).all()

    if not products:
        return api_response(message="No products found", status_code=404)
    
    data = [{
        "id": product.id,
        "name": product.vName,
        "price": float(product.fPrice),
        "description": product.tDescription,
        "category": {
                "id": product.iCategoryId,
                "name": product.category.vName if product.category else ""            
            }
        }
          for product in products]
    payload = generate_pagination(total_items, request.items_per_page, request.page)
    return api_response(data=data, payload=payload, status_code=200)

@router.get("/{product_id}")
async def get_product(product_id: int, db:Session=Depends(get_db)):
    product = Product.get_by_id(db,product_id)
    if not product:
        return api_response(message="Product does not exists", status_code=400)
    product = Product.query(db).filter(Product.id == product_id).options(joinedload(Product.category)).first()
    data = {
            "id" : product.id, 
            "name": product.vName,
            "price": float(product.fPrice),
            "description": product.tDescription,
            "category": {
                "id": product.iCategoryId,
                "name": product.category.vName if product.category else ""
            }
        }
    return api_response(data=data, status_code=200)


@router.post("/create")
async def create_product(request: ProductRequest, db:Session=Depends(get_db)):
    category = Category.get_by_id(db, request.category_id)
    if not category:
        return api_response(message="Category does not exists", status_code=400)    

    product = Product.get_by_name(db, request.name, category.id)
    if product:
        return api_response(message="Product already exists", status_code=400)
    
    newProduct = Product(
        vName=request.name, 
        fPrice=request.price if request.price is not None else 0, 
        tDescription=request.description if request.description is not None else "", 
        iCategoryId=category.id
    )
    
    db.add(newProduct)
    db.commit()

    return api_response(message="Product created successfully", status_code=200)


@router.post("/update/{product_id}")
async def update_product(request: ProductRequest, product_id: int, db:Session=Depends(get_db)):
    category = Category.get_by_id(db, request.category_id)
    if not category:
        return api_response(message="Category does not exists", status_code=400)

    product = Product.get_by_id(db,product_id)
    if not product:
        return api_response(message="Product does not exists", status_code=400)

    productExist = Product.query(db).filter(Product.vName == request.name, Product.id != product_id, Product.iCategoryId == category.id).first()
    if productExist:
        return api_response(message="Product already exists", status_code=400)

    product.vName = request.name
    product.fPrice = request.price if request.price is not None else 0
    product.tDescription = request.description if request.description is not None else ""
    product.iCategoryId = category.id

    db.commit()

    return api_response(message="Product updated successfully", status_code=200)


@router.delete("/delete/{product_id}")
async def delete_product(product_id: int, db:Session=Depends(get_db)):
    product = Product.get_by_id(db,product_id)
    if not product:
        return api_response(message="Product does not exists", status_code=400)
    
    product.deleted_at = func.now()
    db.commit()

    return api_response(message="Product deleted successfully", status_code=200)
