from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import reviews as controller
from ..dependencies.database import get_db
from ..schemas import reviews as schema

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=schema.Review)
def create(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=list[schema.Review])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Review)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.Review)
def update(item_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)
