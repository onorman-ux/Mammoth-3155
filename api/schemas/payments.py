from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    order_id: int
    payment_type: str
    transaction_status: str = "pending"
    transaction_id: Optional[str] = None
    amount: Decimal
    card_last_four: Optional[str] = None
    paid_at: Optional[datetime] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_type: Optional[str] = None
    transaction_status: Optional[str] = None
    transaction_id: Optional[str] = None
    amount: Optional[Decimal] = None
    card_last_four: Optional[str] = None
    paid_at: Optional[datetime] = None


class Payment(PaymentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
