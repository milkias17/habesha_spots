from datetime import datetime, timedelta
from typing import Optional

from dotenv import dotenv_values
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

import crud
import models
import schemas
from db import get_db
from hashing import verify_password

config = dotenv_values(".env")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

auth_router = APIRouter(prefix="/api")


async def authenticate_user(username, password, db: Session) -> models.User:
    user = await crud.get_user_by_username(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> dict:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(weeks=12)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"]
    )
    return encoded_jwt


async def authenticate_access_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    decoded = jwt.decode(token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
    user = db.query(models.User).get(decoded["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    return user


@auth_router.post("/token")
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    weeks = str(config["ACCESS_TOKEN_EXPIRE_WEEKS"])
    access_token_expires = timedelta(int(weeks))
    access_token = await create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=schemas.User)
async def get_current_user(user: models.User = Depends(authenticate_access_token)):
    return schemas.User.from_orm(user)


@auth_router.post("/user")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if await crud.get_user_by_username(
        user.username, db
    ) or await crud.get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or Username already in use",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return schemas.User.from_orm(await crud.create_user(user, db))


@auth_router.get("/user")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = await crud.get_user(user_id, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )

    return schemas.User.from_orm(user)
