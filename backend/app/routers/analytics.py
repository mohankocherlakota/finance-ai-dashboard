from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AnalyticsSummary
from app.services import analytics_service as analytics
from app.services.transaction_service import list_transactions


router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummary)
def summary(db: Session = Depends(get_db)):
    txs = list_transactions(db)
    return AnalyticsSummary(
        income=analytics.total_income(txs),
        expenses=analytics.total_expenses(txs),
        net_cash_flow=analytics.net_cash_flow(txs),
        savings_rate=analytics.savings_rate(txs),
        mom_change=analytics.month_over_month_comparison(txs),
        debt_payments=analytics.debt_payment_total(txs),
    )


@router.get("/monthly")
def monthly(db: Session = Depends(get_db)):
    return analytics.monthly_income_vs_expenses(list_transactions(db))


@router.get("/categories")
def categories(db: Session = Depends(get_db)):
    return analytics.category_spending(list_transactions(db))


@router.get("/merchants")
def merchants(db: Session = Depends(get_db)):
    return analytics.top_merchants(list_transactions(db))


@router.get("/recurring")
def recurring(db: Session = Depends(get_db)):
    return analytics.recurring_transactions(list_transactions(db))
