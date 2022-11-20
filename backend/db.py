from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

config = dotenv_values("backend/.env")

# SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@localhost/chess?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL = "sqlite:///dev_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
