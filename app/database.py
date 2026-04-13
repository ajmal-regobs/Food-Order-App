import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Orders database
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DATABASE", "food_orders")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Menu database
MENU_POSTGRES_USER = os.getenv("MENU_POSTGRES_USER", "postgres")
MENU_POSTGRES_PASSWORD = os.getenv("MENU_POSTGRES_PASSWORD", "postgres")
MENU_POSTGRES_HOST = os.getenv("MENU_POSTGRES_HOST", "localhost")
MENU_POSTGRES_PORT = os.getenv("MENU_POSTGRES_PORT", "5432")
MENU_POSTGRES_DB = os.getenv("MENU_POSTGRES_DATABASE", "menu_db")

MENU_DATABASE_URL = (
    f"postgresql://{MENU_POSTGRES_USER}:{MENU_POSTGRES_PASSWORD}"
    f"@{MENU_POSTGRES_HOST}:{MENU_POSTGRES_PORT}/{MENU_POSTGRES_DB}"
)

menu_engine = create_engine(MENU_DATABASE_URL)
MenuSessionLocal = sessionmaker(bind=menu_engine)


class MenuBase(DeclarativeBase):
    pass


def get_menu_db():
    db = MenuSessionLocal()
    try:
        yield db
    finally:
        db.close()
