from pydantic import BaseModel, EmailStr, validator
import re


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
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
