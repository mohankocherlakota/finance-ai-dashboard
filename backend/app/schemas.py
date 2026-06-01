from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class AccountRead(BaseModel):
    id: int
    plaid_account_id: str
    name: str
    type: str
    subtype: str
    mask: str

    model_config = {"from_attributes": True}


class TransactionRead(BaseModel):
    id: int
    plaid_transaction_id: str
    date: date
    name: str
    merchant_name: str
    amount: float
    category_primary: str
    category_detailed: str
    account_id: int
    pending: bool

    model_config = {"from_attributes": True}


class LinkTokenResponse(BaseModel):
    link_token: str


class ExchangePublicTokenRequest(BaseModel):
    public_token: str


class MessageResponse(BaseModel):
    message: str


class AnalyticsSummary(BaseModel):
    income: float
    expenses: float
    net_cash_flow: float
    savings_rate: float
    mom_change: Dict[str, float]
    debt_payments: float


class InsightResponse(BaseModel):
    observations: List[str]
    risks: List[str]
    recommended_actions: List[str]
    budget_adjustment: str
    debt_payoff_suggestion: str
    motivational_summary: str
    disclaimer: str = "This is not financial advice."


class DebtPayoffRequest(BaseModel):
    loan_balance: float = Field(gt=0)
    interest_rate: float = Field(ge=0)
    monthly_payment: float = Field(gt=0)
    extra_payment: float = Field(default=0, ge=0)


class DebtScenario(BaseModel):
    monthly_payment: float
    months: Optional[int]
    total_interest: float
    payoff_date: Optional[str]


class DebtPayoffResponse(BaseModel):
    baseline: DebtScenario
    requested: DebtScenario
    scenarios: List[DebtScenario]


class SeedResponse(BaseModel):
    accounts: int
    transactions: int


class GenericPayload(BaseModel):
    data: Any
