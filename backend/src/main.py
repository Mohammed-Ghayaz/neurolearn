from fastapi import FastAPI
import uvicorn
from .routes import dummy_route

app = FastAPI()

app.include_router(dummy_route.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
