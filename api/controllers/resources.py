<<<<<<< HEAD
from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import resources as model

MODEL = model.Resource


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
=======
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, resource):
    db_resource = models.Resource(
        resource_item=resource.item,
        resource_amount=resource.amount
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

def update(db: Session, resource_id, resource):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    update_data = resource.model_dump(exclude_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    db.commit()
    return db_resource.first()

def delete(db: Session, resource_id):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    db_resource.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
>>>>>>> origin/main
