from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    special_instructions: Optional[str] = None


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    special_instructions: Optional[str] = None


class OrderDetail(OrderDetailBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
