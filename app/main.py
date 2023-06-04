from fastapi import FastAPI

from app.auth import router as auth_router
from app.routes import router

app = FastAPI(title="Calorties API Docs")

app.include_router(auth_router)
app.include_router(router)
