from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from models.dbsession import get_db
from sqlalchemy.orm import Session
from requests.register import RegisterRequest
from requests.login import LoginRequest
from models.users import User
from utility.password import get_hashed_password, verify_password
from utility.response import api_response
from utility.jwt import create_access_token
from requests.forget_password import ForgetPasswordRequest
from requests.set_new_password import SetNewPasswordRequest
from requests.update_profile import UpdateProfileRequest
from utility.jwt import verify_token
from utility.upload_profile import upload_profile_image

router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, db: Session=Depends(get_db)):
    # user = User.query(db).filter(User.email == request.email).first()
    user = User.get_by_email(db, request.email)
    if user:
        return api_response(message="User already exist", status_code=400)
    
    hashedPassword = get_hashed_password(request.password)
    user = User(email=request.email, password=hashedPassword)
    db.add(user)
    db.commit()
    db.refresh(user)

    result = {
        "id" : user.id,
        "email" : user.email
    }
    return api_response(message="User registered successfully", status_code=200, data=result)
    


@router.post("/forget-password")
def forgot_password(request :ForgetPasswordRequest, db:Session=Depends(get_db)):
    # user = User.query(db).filter(User.email == request.email).first()
    user = User.get_by_email(db, request.email)
    if not user:
        return api_response(message="User not found", status_code=400)
    

    # Send Email verification email from here

    return {"message": "Verification Email sent successfully"}


@router.post("/set-new-password")
def set_new_password(request:SetNewPasswordRequest, db:Session=Depends(get_db)):
    
    user = User.query(db).filter(User.email == request.email).first()

    if not user:
        return api_response(message="User not found", status_code=400)
    
    if request.code != 1234:
        return api_response(message="Invalid verification code", status_code=400)
    
    hashedPassword = get_hashed_password(request.password)
    user.password = hashedPassword
    db.commit()
    
    return api_response(message="Password changed successfully", status_code=200)


@router.post("/login")
def login(request: LoginRequest, db:Session=Depends(get_db)):
    
    # Alternative way of using db session
    # from models.database import SessionLocal
    # db = SessionLocal()

    user = User.get_by_email(db, request.email)
    if not user:
        return api_response(message="User not found", status_code=400)

    if not verify_password(request.password, user.password):
        return api_response(message="Invalid password", status_code=400)

    token = create_access_token({"id": user.id, "email": user.email})
    
    return api_response({"token":token},message="User logged in successfully", status_code=200)

@router.post("/update-profile")
def update_profile(request: UpdateProfileRequest = Depends(), db:Session=Depends(get_db), auth_user_id: int = Depends(verify_token)):    
    
    user = User.get_by_id(db, auth_user_id)

    if request.firstname:
        user.vFirstName = request.firstname

    if request.lastname:
        user.vLastName = request.lastname

    if request.profile:
        # Handle file upload
        uploadResult = upload_profile_image(request.profile)
        if not uploadResult:
            raise HTTPException(status_code=500, detail="Failed to upload profile image")

        # Update the database with the uploaded file's name
        user.vProfileImage = request.profile.filename

    db.commit()
    db.refresh(user)

    return api_response(message="User profile updated successfully", status_code=200)


@router.get("/logout")
def logout():
    # Not Needed because token will be expired
    return {"message": "User logged out successfully"}
