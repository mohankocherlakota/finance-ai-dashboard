from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import MessageResponse, SeedResponse, TransactionRead
from app.services.transaction_service import list_transactions, reset_data, seed_mock_data


router = APIRouter()


@router.get("", response_model=list[TransactionRead])
def get_transactions(db: Session = Depends(get_db)):
    return list_transactions(db)


@router.post("/seed", response_model=SeedResponse)
def seed(db: Session = Depends(get_db)):
    return seed_mock_data(db)


@router.post("/reset", response_model=MessageResponse)
def reset(db: Session = Depends(get_db)):
    reset_data(db)
    return MessageResponse(message="Data reset complete")
