from fastapi import Form, File, UploadFile
from typing import Optional
from pydantic import BaseModel, validator, Field
from fastapi.exceptions import HTTPException
import re

class UpdateProfileRequest:
    def __init__(
        self,
        firstname: Optional[str] = Form(None),
        lastname: Optional[str] = Form(None),
        profile: Optional[UploadFile] = File(None),
    ):
        # Validate firstname
        if firstname and not re.match(r"^[A-Za-z]+$", firstname):
            raise HTTPException(
                status_code=422, detail="Firstname should contain only alphabetic characters"
            )
        self.firstname = firstname

        # Validate lastname
        if lastname and not re.match(r"^[A-Za-z]+$", lastname):
            raise HTTPException(
                status_code=422, detail="Lastname should contain only alphabetic characters"
            )
        self.lastname = lastname

        # Validate profile file
        if profile:
            max_size = 10 * 1024 * 1024  # 10 MB
            profile.file.seek(0, 2)  # Move pointer to end of the file
            file_size = profile.file.tell()  # Get the file size
            profile.file.seek(0)  # Reset pointer to the beginning
            if file_size > max_size:
                raise HTTPException(status_code=422, detail="File size exceeds 10 MB")

            allowed_content_types = {"image/jpeg", "image/png"}
            if profile.content_type not in allowed_content_types:
                raise HTTPException(
                    status_code=422,
                    detail="Invalid file type. Only .jpeg and .png files are allowed",
                )
        self.profile = profile
