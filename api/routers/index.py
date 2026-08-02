from . import (
    orders,
    order_details,
    resources,
    menu_items,
    recipes,
    promotions,
)


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(resources.router)
    app.include_router(menu_items.router)
    app.include_router(recipes.router)
    app.include_router(promotions.router)