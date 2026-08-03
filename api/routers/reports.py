from datetime import date, datetime, time
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.menu_items import MenuItem
from ..models.order_details import OrderDetail
from ..models.orders import Order
from ..models.payments import Payment
from ..models.reviews import Review

router = APIRouter(prefix="/reports", tags=["Staff Reports"])

@router.get("/daily-revenue")
def daily_revenue(day: date, db: Session = Depends(get_db)):
    start=datetime.combine(day,time.min); end=datetime.combine(day,time.max)
    total=db.query(func.coalesce(func.sum(Payment.amount),0)).join(Order,Payment.order_id==Order.id).filter(Payment.transaction_status=="paid",Order.order_date.between(start,end)).scalar()
    return {"date": day, "revenue": total}

@router.get("/menu-popularity")
def menu_popularity(db: Session = Depends(get_db)):
    rows=(db.query(MenuItem.id,MenuItem.name,func.coalesce(func.sum(OrderDetail.quantity),0).label("quantity_ordered"))
          .outerjoin(OrderDetail,MenuItem.id==OrderDetail.menu_item_id).group_by(MenuItem.id,MenuItem.name)
          .order_by(func.coalesce(func.sum(OrderDetail.quantity),0).asc()).all())
    return [{"menu_item_id":r.id,"name":r.name,"quantity_ordered":int(r.quantity_ordered)} for r in rows]

@router.get("/complaints")
def complaints(max_rating: int = 2, db: Session = Depends(get_db)):
    rows=(db.query(Review,MenuItem).join(MenuItem,Review.menu_item_id==MenuItem.id).filter(Review.rating<=max_rating).order_by(Review.created_at.desc()).all())
    return [{"review_id":r.id,"dish":m.name,"rating":r.rating,"reason":r.review_text,"created_at":r.created_at} for r,m in rows]
