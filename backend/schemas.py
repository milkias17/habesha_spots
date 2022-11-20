from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class PlaceCreate(BaseModel):
    type: str
    location: str
    name: str

    class Config:
        orm_mode = True


class Place(PlaceCreate):
    user_id: int
    reviews: list


class ReviewCreate(BaseModel):
    place_id: int
    rating: float

    class Config:
        orm_mode = True


class Review(ReviewCreate):
    id: int
    user_id: int
