from fastapi import APIRouter, Depends
from ..db.database import get_db

router = APIRouter()

@router.get("/dummy")
def dummy_route(db=Depends(get_db)):
    return {"db": "connected"}