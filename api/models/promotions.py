from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    discount_type = Column(String(20), nullable=False, default="percentage")
    discount_value = Column(Numeric(10, 2), nullable=False, default=0)
    expiration_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    orders = relationship("Order", back_populates="promotion")
