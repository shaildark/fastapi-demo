from fastapi import APIRouter, Depends, HTTPException
from models.dbsession import get_db
from middleware.jwt_auth import JWTAuthRoute
from fastapi import Request
from requests.category.list_category import ListCategoryRequest
from requests.category.category_request import CategoryRequest
from models.category import Category
from models.product import Product
from sqlalchemy.orm import Session
from utility.response import api_response
from utility.pagination import generate_pagination
from sqlalchemy import func


# router = APIRouter(route_class=JWTAuthRoute)
router = APIRouter(
    prefix="/categories",
)


@router.post("/list")
async def list_product_categories(request: ListCategoryRequest, db:Session=Depends(get_db)):
    query = Category.query(db)

    if request.search:
        query = query.filter(Category.vName.ilike(f"%{request.search}%"))
    
    total_items = query.count()
    categories = query.offset((request.page - 1) * request.items_per_page).limit(request.items_per_page).all()

    if not categories:
        return api_response(message="No categories found", status_code=404)
    
    data = [{"id": category.id, "name": category.vName} for category in categories]
    payload = generate_pagination(total_items, request.items_per_page, request.page)
    return api_response(data=data, payload=payload, status_code=200)


@router.get("/{category_id}")
async def get_product_category(category_id: int, db:Session=Depends(get_db)):
    category = Category.get_by_id(db, category_id)

    if not category:
        return api_response(message="No category found", status_code=404)
    
    data = {"id": category.id, "name": category.vName}
    return api_response(data=data, status_code=200)



@router.post("/create")
async def create_product_category(request: CategoryRequest, db:Session=Depends(get_db)):
    category = Category.get_by_name(db, request.name)
    
    if category:
        return api_response(message="Category already exists", status_code=400)    

    category = Category(vName=request.name)
    db.add(category)
    db.commit()

    return api_response(message="Category created successfully", status_code=200)


@router.post("/update/{category_id}")
async def update_product_category(request: CategoryRequest, category_id: int, db:Session=Depends(get_db)):
    category = Category.get_by_id(db, category_id)
    
    if not category:
        return api_response(message="Category does not exists", status_code=400)
    
    category_exist = db.query(Category).filter(Category.vName == request.name, Category.id != category_id).first()

    if category_exist:
        return api_response(message="Category already exists", status_code=400)
    
    category.vName = request.name
    db.commit()

    return api_response(message="Category updated successfully", status_code=200)


@router.delete("/delete/{category_id}")
async def delete_product_category(category_id: int, db:Session=Depends(get_db)):
    category = Category.get_by_id(db, category_id)    
    if not category:
        return api_response(message="Category does not exists", status_code=400)
    
    product = Product.query(db).filter(Product.iCategoryId == category_id).first()    
    if product:
        return api_response(message="Category is associated with a product", status_code=400)
    
    category.deleted_at = func.now()
    db.commit()

    return api_response(message="Category deleted successfully", status_code=200)
