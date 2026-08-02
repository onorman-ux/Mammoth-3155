from . import (
    customers,
    menu_items,
    resources,
    recipes,
    promotions,
    orders,
    order_details,
    payments,
    reviews,
)

from ..dependencies.database import Base, engine


def index():
    Base.metadata.create_all(bind=engine)
