from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from auth import authenticate_access_token
from db import get_db

places_router = APIRouter(prefix="/api")


@places_router.post("/place")
def create_place(
    place_data: schemas.PlaceCreate,
    user: models.User = Depends(authenticate_access_token),
    db: Session = Depends(get_db),
):
    place = models.Place(**place_data.__dict__, user_id=user.id)
    db.add(place)
    db.commit()
    return schemas.PlaceCreate.from_orm(place)


@places_router.get("/places")
def get_places(
    user: models.User = Depends(authenticate_access_token),
):
    return user.places


@places_router.get("/place/{place_id}")
def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter_by(id=place_id).first()

    return schemas.Place.from_orm(place)
