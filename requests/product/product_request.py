from pydantic import BaseModel, Field
from typing import Optional

class ProductRequest(BaseModel):
    name: Optional[str] = Field(... , min_length=1)
    price: Optional[float] = Field(... , gt=0)
    description: Optional[str] = Field(None)
    category_id: int