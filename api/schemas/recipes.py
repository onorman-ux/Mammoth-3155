from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RecipeBase(BaseModel):
    menu_item_id: int
    resource_id: int
    amount: Decimal


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[Decimal] = None


class Recipe(RecipeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
