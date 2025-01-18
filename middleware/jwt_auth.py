from fastapi.routing import APIRoute
from fastapi import Request, HTTPException, status
from typing import Callable
from models.users import User
from models.database import SessionLocal
from utility.response import jwt_error_response
import jwt  
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Shailendra")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_EXPIRATION_MINUTES", 1440)
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

class JWTAuthRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            authorization: str = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=jwt_error_response(message="Authorization header missing.", status_code=status.HTTP_401_UNAUTHORIZED),
                )
            
            try:
                scheme, token = authorization.split()
                
                if scheme.lower() != "bearer":                        
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=jwt_error_response(message="Invalid authentication scheme.", status_code=status.HTTP_401_UNAUTHORIZED),
                    )
                
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])                   
                
                if "id" not in payload or "email" not in payload:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=jwt_error_response(message="Invalid JWT token.", status_code=status.HTTP_401_UNAUTHORIZED),
                    )
                
                db = SessionLocal()
                user = User.query(db).filter(User.email == payload['email']).first()
                
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=jwt_error_response(message="User not found.", status_code=status.HTTP_401_UNAUTHORIZED),
                    )
                
                # Attach values to request state and access value like this print(request.state.auth_user_id)
                request.state.auth_user_id = int(user.id)
                request.state.auth_user_email = user.email

            except (ValueError, jwt.PyJWTError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=jwt_error_response(message="Invalid token or expired token.", status_code=status.HTTP_401_UNAUTHORIZED),
                )
            
            return await original_route_handler(request)

        return custom_route_handler
