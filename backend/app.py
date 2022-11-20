from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db
from auth import auth_router
from places import places_router
from reviews import reviews_router

db.Base.metadata.create_all(bind=db.engine)

origins = ["*"]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(places_router)
app.include_router(reviews_router)


@app.get("/")
async def hello():
    return {"message": "Hello, World!"}
