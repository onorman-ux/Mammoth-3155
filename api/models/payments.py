from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        unique=True,
        nullable=False,
    )

    payment_type = Column(
        String(50),
        nullable=False,
    )

    transaction_status = Column(
        String(50),
        nullable=False,
        default="pending",
    )

    transaction_id = Column(
        String(150),
        unique=True,
        nullable=True,
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False,
    )

    card_last_four = Column(
        String(4),
        nullable=True,
    )

    paid_at = Column(
        DateTime,
        nullable=True,
    )

    order = relationship(
        "Order",
        back_populates="payment",
    )
