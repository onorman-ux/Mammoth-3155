from sqlalchemy import Boolean, Column, Integer, Numeric, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    calories = Column(Integer, nullable=True)
    category = Column(String(100), nullable=True)
    is_available = Column(Boolean, nullable=False, default=True)

    recipes = relationship(
        "Recipe",
        back_populates="menu_item",
        cascade="all, delete-orphan",
    )

    order_details = relationship(
        "OrderDetail",
        back_populates="menu_item",
    )
