from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import recipes as controller
from ..dependencies.database import get_db
from ..schemas import recipes as schema

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("/", response_model=schema.Recipe)
def create(request: schema.RecipeCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=list[schema.Recipe])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Recipe)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.Recipe)
def update(item_id: int, request: schema.RecipeUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)
