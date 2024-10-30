from fastapi import APIRouter, HTTPException, Depends, status
from ..models import Dht11Record
from sqlalchemy.orm import Session
from typing import Annotated
from ..dependencies import get_db
from ..services.process import pull_and_save

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/api/dht11")

@router.put('/records')
async def process_data():
    """Save records from queue"""
    messages_saved = pull_and_save()
    return {'message': f"Processed {messages_saved} record(s)."}

@router.get("/records", status_code= status.HTTP_200_OK)
async def read_records(db: db_dependency):
    records = db.query(Dht11Record).all()
    if records is None:
        raise HTTPException(status_code=404, detail='No not found')
    return records