import jwt
import datetime
from fastapi import HTTPException, Request, status
from utility.response import jwt_error_response
from models.database import SessionLocal
from models.users import User
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Shailendra")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_EXPIRATION_MINUTES", 1440)
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def create_access_token(data: dict, expires_delta: datetime.timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=jwt_error_response(status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid or missing token"),
            )
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        db = SessionLocal()
        user = User.get_by_email(db, payload['email'])        
        if not user:
            raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=jwt_error_response(message="User not found.", status_code=status.HTTP_401_UNAUTHORIZED),
                        )
        return int(user.id)
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=jwt_error_response(status_code=status.HTTP_401_UNAUTHORIZED, message=f"Token verification failed: {str(e)}"),
            )
