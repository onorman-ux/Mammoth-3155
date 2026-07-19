from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True,
    )

    promotion_id = Column(
        Integer,
        ForeignKey("promotions.id"),
        nullable=True,
    )

    guest_name = Column(String(100), nullable=True)
    guest_email = Column(String(150), nullable=True)
    guest_phone = Column(String(25), nullable=True)

    order_date = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    tracking_number = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    order_status = Column(
        String(50),
        nullable=False,
        default="pending",
    )

    order_type = Column(
        String(30),
        nullable=False,
        default="takeout",
    )

    delivery_address = Column(String(255), nullable=True)

    total_price = Column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    customer = relationship(
        "Customer",
        back_populates="orders",
    )

    promotion = relationship(
        "Promotion",
        back_populates="orders",
    )

    order_details = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    review = relationship(
        "Review",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )
