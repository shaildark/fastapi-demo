from pydantic import BaseModel, EmailStr, validator, ValidationError
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import re

class SetNewPasswordRequest(BaseModel):
    email: EmailStr
    password: str
    code: int

    @validator("password")
    def validate_password(cls, value):
        """Validate password for length, digits, uppercase, lowercase, and special symbols."""
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value
    
    # @app.exception_handler(ValidationError)
    # async def validation_exception_handler(request: Request, exc: ValidationError):
    #     errors = [
    #         {"field": e["loc"][-1], "message": e["msg"]} for e in exc.errors()
    #     ]
    #     return JSONResponse(
    #         status_code=422,
    #         content={"detail": "Validation Error", "errors": errors},
    #     )