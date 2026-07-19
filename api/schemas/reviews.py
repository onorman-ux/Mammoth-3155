from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    order_id: int
    customer_id: Optional[int] = None
    rating: int = Field(ge=1, le=5)
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
