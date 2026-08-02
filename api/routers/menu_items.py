from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import orders, order_details, resources, menu_items
from ..controllers import menu_items as controller
from ..dependencies.database import get_db
from ..schemas import menu_items as schema

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])


@router.post("/", response_model=schema.MenuItem)
def create(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=list[schema.MenuItem])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.MenuItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)


@router.get("/search/", response_model=list[schema.MenuItem])
def search(name: str | None = None, category: str | None = None, available_only: bool = True, db: Session = Depends(get_db)):
    from ..models.menu_items import MenuItem
    query = db.query(MenuItem)
    if name:
        query = query.filter(MenuItem.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(MenuItem.category.ilike(f"%{category}%"))
    if available_only:
        query = query.filter(MenuItem.is_available.is_(True))
    return query.all()

def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(resources.router)
    app.include_router(menu_items.router)