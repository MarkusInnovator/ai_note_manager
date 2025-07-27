from fastapi import FastAPI
from .auth.routes import router as auth_router
from .models import Base
from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
