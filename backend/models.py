from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    reviews = relationship("Reviews", back_populates="user")
    places = relationship("Place", back_populates="user")


class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(25), nullable=False)
    location = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)

    reviews = relationship("Reviews", back_populates="place")
    user = relationship("User", back_populates="places")


class Reviews(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    rating = Column(Float, nullable=False)

    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
