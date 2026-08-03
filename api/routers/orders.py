from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import orders as controller
from ..dependencies.database import get_db
from ..models.orders import Order as OrderModel
from ..schemas import orders as schema

router = APIRouter(tags=["Orders"], prefix="/orders")

@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)): return controller.create(db, request)

@router.post("/checkout", response_model=schema.Order, summary="Place a guest or customer order")
def checkout(request: schema.CheckoutOrderCreate, db: Session = Depends(get_db)): return controller.checkout(db, request)

@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)): return controller.read_all(db)

@router.get("/date-range", response_model=list[schema.Order])
def date_range(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    if start_date > end_date: from fastapi import HTTPException; raise HTTPException(400, "start_date must be before end_date")
    return db.query(OrderModel).filter(OrderModel.order_date.between(start_date, end_date)).all()

@router.get("/track/{tracking_number}", response_model=schema.Order)
def track(tracking_number: str, db: Session = Depends(get_db)): return controller.track(db, tracking_number)

@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)): return controller.read_one(db, item_id)

@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)): return controller.update(db, item_id, request)

@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, db: Session = Depends(get_db)): return controller.delete(db, item_id)
