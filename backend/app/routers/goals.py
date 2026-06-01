from fastapi import APIRouter

from app.schemas import DebtPayoffRequest, DebtPayoffResponse
from app.services.goals_service import calculate_debt_scenarios


router = APIRouter()


@router.post("/debt-payoff", response_model=DebtPayoffResponse)
def debt_payoff(payload: DebtPayoffRequest):
    return calculate_debt_scenarios(
        balance=payload.loan_balance,
        interest_rate=payload.interest_rate,
        monthly_payment=payload.monthly_payment,
        extra_payment=payload.extra_payment,
    )
