from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    tracking_number: str
    order_status: str = "pending"
    order_type: str = "takeout"
    delivery_address: Optional[str] = None
    total_price: Decimal


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    tracking_number: Optional[str] = None
    order_status: Optional[str] = None
    order_type: Optional[str] = None
    delivery_address: Optional[str] = None
    total_price: Optional[Decimal] = None


class Order(OrderBase):
    id: int
    order_date: datetime

    model_config = ConfigDict(from_attributes=True)


class CheckoutItem(BaseModel):
    menu_item_id: int
    quantity: int
    special_instructions: Optional[str] = None


class CheckoutOrderCreate(BaseModel):
    customer_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    order_type: str = "takeout"
    delivery_address: Optional[str] = None
    promo_code: Optional[str] = None
    items: list[CheckoutItem]
