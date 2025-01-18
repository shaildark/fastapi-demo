from fastapi import FastAPI, Request
from routes.auth_routes import router as auth_router
from routes.product_routes import router as product_router
from routes.category_routes import router as category_router
from models.database import SessionLocal
from fastapi.exceptions import RequestValidationError
from utility.response import api_response
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth_router,tags=["Auth"])
app.include_router(product_router,tags=["Product"])
app.include_router(category_router,tags=["Category"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            # "type": error.get("type", "validation_error"),
            "field": error["loc"][-1],
            "message": error["msg"],
            # "input": error.get("input", None),
        })
    return api_response(message="Validation Error", status_code=422, errors=errors)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def helloworld():
    return {"message": "Hello World"}


