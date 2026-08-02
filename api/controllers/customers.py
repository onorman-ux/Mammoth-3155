from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import customers as model

MODEL = model.Customer


def _db_error(db, exc):
    db.rollback()
    detail = str(getattr(exc, "orig", exc))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def create(db: Session, request):
    item = MODEL(**request.model_dump())
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as exc:
        _db_error(db, exc)


def read_all(db: Session):
    return db.query(MODEL).all()


def read_one(db: Session, item_id: int):
    item = db.query(MODEL).filter(MODEL.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def update(db: Session, item_id: int, request):
    item = read_one(db, item_id)
    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    try:
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as exc:
        _db_error(db, exc)


def delete(db: Session, item_id: int):
    item = read_one(db, item_id)
    try:
        db.delete(item)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as exc:
        _db_error(db, exc)
