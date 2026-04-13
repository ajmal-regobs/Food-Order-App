from fastapi import FastAPI

from app.database import Base, MenuBase, engine, menu_engine
from app.routes import router

Base.metadata.create_all(bind=engine)
MenuBase.metadata.create_all(bind=menu_engine)

app = FastAPI(title="Food Order API")
app.include_router(router)
