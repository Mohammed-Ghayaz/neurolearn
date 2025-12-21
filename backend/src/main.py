from fastapi import FastAPI
import uvicorn
from .routes import dummy_route, auth_route
from .db.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_route.router, prefix="/api/v1/auth")
app.include_router(dummy_route.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
