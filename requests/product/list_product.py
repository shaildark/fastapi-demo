from pydantic import BaseModel, Field
from typing import Optional


class ListProductRequest(BaseModel):
    search : Optional[str] = Field(default=None)
    category_id : Optional[int] = Field(default=None)
    page : Optional[int] = Field(default=1)
    items_per_page : Optional[int] = Field(default=10)