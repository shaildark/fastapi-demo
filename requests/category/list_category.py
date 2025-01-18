from pydantic import BaseModel, Field
from typing import Optional


class ListCategoryRequest(BaseModel):
    search : Optional[str] = Field(default=None)
    page : Optional[int] = Field(default=1)
    items_per_page : Optional[int] = Field(default=10)