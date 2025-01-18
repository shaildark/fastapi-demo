from pydantic import BaseModel, Field
from typing import Optional

class CategoryRequest(BaseModel):
    name: Optional[str] = Field(... , min_length=1)