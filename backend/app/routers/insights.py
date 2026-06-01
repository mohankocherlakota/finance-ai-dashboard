from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import InsightResponse
from app.services.ai_insights_service import generate_insights
from app.services.analytics_service import summarize_for_ai
from app.services.transaction_service import list_transactions


router = APIRouter()


@router.post("/generate", response_model=InsightResponse)
def generate(db: Session = Depends(get_db)):
    summarized_data = summarize_for_ai(list_transactions(db))
    return generate_insights(summarized_data)
