from sqlalchemy.orm import Session

import models
import schemas
from hashing import hash_password


async def get_user(user_id: int, db: Session):
    return db.query(models.User).filter_by(id=user_id).first()


async def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter_by(email=email).first()


async def get_user_by_username(username: str, db: Session):
    return db.query(models.User).filter_by(username=username).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(user: schemas.UserCreate, db: Session):
    user = models.User(
        username=user.username,
        first_name=user.first_name.capitalize(),
        last_name=user.last_name.capitalize(),
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
