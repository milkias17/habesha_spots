import models
import schemas
from auth import authenticate_access_token
from db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

reviews_router = APIRouter(prefix="/api")


@reviews_router.post("/review")
def create_review(
    review_data: schemas.ReviewCreate,
    user: models.User = Depends(authenticate_access_token),
    db: Session = Depends(get_db),
):
    review = models.Reviews(**review_data.__dict__, user_id=user.id)
    db.add(review)
    db.commit()
    return schemas.ReviewCreate.from_orm(review)


@reviews_router.get("/reviews")
def get_reviews(
    user: models.User = Depends(authenticate_access_token),
):
    return user.reviews


@reviews_router.get("/review/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Reviews).filter_by(id=review_id).first()

    return schemas.Review.from_orm(review)
