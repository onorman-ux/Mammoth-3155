from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.menu_items import MenuItem
from ..models.order_details import OrderDetail
from ..models.orders import Order
from ..models.promotions import Promotion
from ..models.recipes import Recipe
from ..models.resources import Resource


def create(db: Session, request):
    item = Order(**request.model_dump())
    try:
        db.add(item); db.commit(); db.refresh(item); return item
    except SQLAlchemyError as exc:
        db.rollback(); raise HTTPException(400, str(getattr(exc, "orig", exc)))


def checkout(db: Session, request):
    if not request.items:
        raise HTTPException(400, "An order must contain at least one menu item")
    if request.order_type not in {"takeout", "delivery"}:
        raise HTTPException(400, "order_type must be 'takeout' or 'delivery'")
    if request.order_type == "delivery" and not request.delivery_address:
        raise HTTPException(400, "A delivery address is required for delivery orders")
    if request.customer_id is None and not request.guest_name:
        raise HTTPException(400, "Guest name is required when no customer account is used")

    subtotal = Decimal("0.00")
    detail_rows = []
    needed = {}
    for requested in request.items:
        if requested.quantity <= 0:
            raise HTTPException(400, "Item quantity must be greater than zero")
        menu_item = db.query(MenuItem).filter(MenuItem.id == requested.menu_item_id).first()
        if not menu_item or not menu_item.is_available:
            raise HTTPException(404, f"Menu item {requested.menu_item_id} is unavailable")
        subtotal += Decimal(menu_item.price) * requested.quantity
        detail_rows.append((menu_item, requested))
        recipes = db.query(Recipe).filter(Recipe.menu_item_id == menu_item.id).all()
        for recipe in recipes:
            needed[recipe.resource_id] = needed.get(recipe.resource_id, Decimal("0")) + Decimal(recipe.amount) * requested.quantity

    for resource_id, amount_needed in needed.items():
        resource = db.query(Resource).filter(Resource.id == resource_id).with_for_update().first()
        if not resource:
            raise HTTPException(400, f"Recipe references missing resource {resource_id}")
        if Decimal(resource.amount) < amount_needed:
            raise HTTPException(409, f"Insufficient {resource.item}: required {amount_needed} {resource.unit}, available {resource.amount} {resource.unit}")

    promotion = None
    discount = Decimal("0.00")
    if request.promo_code:
        promotion = db.query(Promotion).filter(func.lower(Promotion.code) == request.promo_code.lower()).first()
        if not promotion or not promotion.is_active:
            raise HTTPException(400, "Promotional code is invalid or inactive")
        if promotion.expiration_date and promotion.expiration_date < datetime.now():
            raise HTTPException(400, "Promotional code has expired")
        value = Decimal(promotion.discount_value)
        if promotion.discount_type == "percentage":
            discount = subtotal * value / Decimal("100")
        elif promotion.discount_type == "fixed":
            discount = value
        else:
            raise HTTPException(400, "Promotion discount_type must be percentage or fixed")

    total = max(Decimal("0.00"), subtotal - discount).quantize(Decimal("0.01"))
    order = Order(
        customer_id=request.customer_id,
        promotion_id=promotion.id if promotion else None,
        guest_name=request.guest_name,
        guest_email=request.guest_email,
        guest_phone=request.guest_phone,
        tracking_number=f"OROS-{uuid4().hex[:10].upper()}",
        order_status="received",
        order_type=request.order_type,
        delivery_address=request.delivery_address,
        total_price=total,
    )
    try:
        db.add(order); db.flush()
        for menu_item, requested in detail_rows:
            db.add(OrderDetail(order_id=order.id, menu_item_id=menu_item.id, quantity=requested.quantity, unit_price=menu_item.price, special_instructions=requested.special_instructions))
        for resource_id, amount_needed in needed.items():
            resource = db.query(Resource).filter(Resource.id == resource_id).first()
            resource.amount = Decimal(resource.amount) - amount_needed
        db.commit(); db.refresh(order); return order
    except SQLAlchemyError as exc:
        db.rollback(); raise HTTPException(400, str(getattr(exc, "orig", exc)))


def read_all(db: Session): return db.query(Order).all()

def read_one(db: Session, item_id: int):
    item=db.query(Order).filter(Order.id==item_id).first()
    if not item: raise HTTPException(404,"Order not found")
    return item

def track(db: Session, tracking_number: str):
    item=db.query(Order).filter(Order.tracking_number==tracking_number).first()
    if not item: raise HTTPException(404,"Tracking number not found")
    return item

def update(db: Session,item_id:int,request):
    item=read_one(db,item_id)
    for k,v in request.model_dump(exclude_unset=True).items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

def delete(db:Session,item_id:int):
    item=read_one(db,item_id); db.delete(item); db.commit(); return Response(status_code=status.HTTP_204_NO_CONTENT)
